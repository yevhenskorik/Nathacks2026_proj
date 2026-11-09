"""
auth.py: login page for the RA On-Shift Helper (Streamlit).

Run the app from this file:  streamlit run auth.py

There is no sign-up form. Accounts are rows in the Supabase table "users", added
by the team. No passwords are stored in this file.

Passwords in the database are salted and hashed with PBKDF2. The plain text
password is never stored.

Settings come from .streamlit/secrets.toml (SUPABASE_URL and SUPABASE_KEY).
"""

import hashlib
import hmac
import json

import streamlit as st

from ui import apply_theme, notice, page_title, site_footer

USERS_TABLE = "users"
PBKDF2_ROUNDS = 200_000


class AccountStoreError(Exception):
    """Raised when the account database cannot be reached."""


def _pbkdf2(password: str, salt_hex: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        PBKDF2_ROUNDS,
    ).hex()


# ---------------------------------------------------------------------------
# Database access
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def _get_client():
    from supabase import create_client

    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def _fetch_db_user(username: str):
    """Return the stored row for a username, or None. Raises AccountStoreError."""
    try:
        response = (
            _get_client()
            .table(USERS_TABLE)
            .select("*")
            .eq("username", username)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        raise AccountStoreError(str(exc)) from exc
    return response.data[0] if response.data else None


# ---------------------------------------------------------------------------
# Login logic
# ---------------------------------------------------------------------------

def authenticate(username: str, password: str):
    """
    Return the user dict on success, otherwise None.
    Raises AccountStoreError when the database cannot be reached.
    """
    username = username.strip().lower()

    row = _fetch_db_user(username)
    if row is None:
        # Hash anyway so response time does not reveal valid usernames.
        _pbkdf2(password, "00" * 16)
        return None

    if hmac.compare_digest(row["password_hash"], _pbkdf2(password, row["salt"])):
        # RAs are shown by username. Students use their display name.
        if row["role"] == "ra":
            name = row["username"]
        else:
            name = row.get("display_name") or row["username"]
        return {"username": row["username"], "role": row["role"], "name": name}
    return None


# ---------------------------------------------------------------------------
# Pages and helpers
# ---------------------------------------------------------------------------

def _render_sign_in_form():
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

    if not submitted:
        return

    if not username or not password:
        st.warning("Enter both a username and a password.")
        return

    try:
        user = authenticate(username, password)
    except AccountStoreError:
        st.error("Could not reach the account database. Check .streamlit/secrets.toml.")
        return

    if user:
        st.session_state["user"] = user
        st.rerun()
    else:
        st.error("Incorrect username or password.")


def show_login():
    """Render the sign in form. Sets st.session_state['user'] on login."""
    apply_theme("560px")  # same green and gold look as both dashboards
    st.markdown(
        """
        <style>
        /* The card already frames the form, so drop the form's own border */
        [data-testid="stForm"] { border: 0 !important; padding: 0 !important; }
        .stApp [data-testid="stTextInputRootElement"] { border-radius: 0 !important; }

        /* Sign in button in the same green as the dashboards */
        .stApp [data-testid="stBaseButton-primaryFormSubmit"],
        .stApp button[kind="primaryFormSubmit"] {
            background-color: #275D38; border: 1px solid #275D38; color: #FFFFFF;
            border-radius: 0 !important; font-weight: 700;
            letter-spacing: 0.06em; text-transform: uppercase; padding: 0.6rem 1.2rem;
        }
        .stApp [data-testid="stBaseButton-primaryFormSubmit"]:hover,
        .stApp button[kind="primaryFormSubmit"]:hover {
            background-color: #1D4529; border-color: #1D4529; color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    page_title("RA On-Shift Helper", "Sign in to report an issue or review reports.")
    notice("In an emergency, call <b>911</b>. This app is not watched in real time.")

    with st.container(key="card_login"):
        st.subheader("Sign in")
        _render_sign_in_form()

    site_footer()


def require_login(allowed_roles=None):
    """
    Gate a page. Returns the logged-in user dict.
    Stops the script and shows the login form if nobody is signed in.
    Pass allowed_roles=["ra"] to restrict a page to certain roles.
    """
    user = st.session_state.get("user")

    if user is None:
        show_login()
        st.stop()

    if allowed_roles and user["role"] not in allowed_roles:
        st.error("Your account does not have access to this page.")
        show_user_sidebar(user)
        st.stop()

    return user


# JavaScript that adds a three-bar menu button to the page. It opens and closes the
# sidebar, so the Log out block always has a way back after it is hidden.
_MENU_BUTTON_JS = r"""
(function () {
  var doc = document;
  var host = window;
  if (host.__raMenuButton) { return; }
  host.__raMenuButton = true;

  var style = doc.createElement('style');
  style.textContent =
    '#ra-menu-btn{position:fixed;top:76px;left:12px;z-index:1000001;width:42px;height:42px;' +
    'display:none;flex-direction:column;justify-content:center;align-items:center;gap:5px;' +
    'background:#275d38;border:0;border-radius:4px;cursor:pointer;padding:0;' +
    'box-shadow:0 2px 6px rgba(0,0,0,0.25);}' +
    '#ra-menu-btn span{display:block;width:22px;height:3px;background:#ffffff;border-radius:1px;}' +
    '#ra-menu-btn:hover{background:#1d4a2c;}';
  doc.head.appendChild(style);

  var btn = doc.createElement('button');
  btn.id = 'ra-menu-btn';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Open or close the menu');
  btn.innerHTML = '<span></span><span></span><span></span>';
  doc.body.appendChild(btn);

  function find(selectors) {
    for (var i = 0; i < selectors.length; i++) {
      var el = doc.querySelector(selectors[i]);
      if (el) { return el.tagName === 'BUTTON' ? el : (el.querySelector('button') || el); }
    }
    return null;
  }

  var EXPAND = ['[data-testid="stExpandSidebarButton"]',
                '[data-testid="stSidebarCollapsedControl"]',
                '[data-testid="collapsedControl"]'];
  var COLLAPSE = ['[data-testid="stSidebarCollapseButton"]'];

  btn.addEventListener('click', function () {
    var sidebar = doc.querySelector('[data-testid="stSidebar"]');
    var collapsed = !!sidebar && (sidebar.getAttribute('data-collapsed') === 'true' ||
                                  sidebar.getAttribute('aria-expanded') === 'false');
    var target = find(collapsed ? EXPAND : COLLAPSE) || find(collapsed ? COLLAPSE : EXPAND);
    if (target) { target.click(); }
  });

  // Show the button only while the sidebar is hidden. The arrow inside the sidebar closes it again.
  host.setInterval(function () {
    var sidebar = doc.querySelector('[data-testid="stSidebar"]');
    var signedIn = !!sidebar && sidebar.textContent.indexOf('Log out') !== -1;
    var hidden = !!sidebar && (sidebar.getAttribute('data-collapsed') === 'true' ||
                               sidebar.getAttribute('aria-expanded') === 'false');
    btn.style.display = (signedIn && hidden) ? 'flex' : 'none';
  }, 300);
})();
"""


def _menu_button():
    """Adds the three-bar menu button once. Needs no setup in the page files."""
    import streamlit.components.v1 as components

    # The code runs inside the main page, not the small helper frame. The helper
    # frame is removed on logout, and code left inside it would stop with it.
    loader = (
        "<script>"
        "var d = window.parent.document;"
        "if (!window.parent.__raMenuLoaded) {"
        "  window.parent.__raMenuLoaded = true;"
        "  var s = d.createElement('script');"
        f"  s.textContent = {json.dumps(_MENU_BUTTON_JS)};"
        "  d.head.appendChild(s);"
        "}"
        "</script>"
    )
    components.html(loader, height=0)


def show_user_sidebar(user):
    """
    Sidebar block with the signed-in name, role, and a logout button.
    Draws once per page run, so a second call from a page file is ignored.
    """
    run_id = st.session_state.get("_run_id")
    if run_id is not None and st.session_state.get("_sidebar_run") == run_id:
        return
    st.session_state["_sidebar_run"] = run_id

    with st.sidebar:
        st.markdown(
            """
            <style>
            /* Keep the hide-sidebar arrow visible, not only on hover */
            [data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarCollapseButton"] button,
            [data-testid="stSidebarHeader"] button {
                opacity: 1 !important;
                visibility: visible !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"**{user['name']}**")
        st.caption(f"Role: {user['role'].upper()}")
        if st.button("Log out", use_container_width=True, key="logout_btn"):
            st.session_state.pop("user", None)
            st.rerun()
        _menu_button()


def main():
    """
    Entry point: streamlit run auth.py
    Shows the login form first. After sign-in, students are sent to the
    student report page in student_app.py. RAs are sent to ra_app.py.
    """
    st.set_page_config(page_title="RA On-Shift Helper", page_icon="🏠")
    st.session_state["_run_id"] = st.session_state.get("_run_id", 0) + 1
    user = require_login()
    if user is None:
        # Happens when the file is run with plain python instead of streamlit.
        print("Run this with: streamlit run auth.py")
        return
    show_user_sidebar(user)

    if user["role"] == "student":
        pages = [st.Page("student_app.py", title="Report an Incident", icon="📝")]
    else:
        pages = [st.Page("ra_app.py", title="RA Dashboard", icon="🗺️")]

    st.navigation(pages).run()


if __name__ == "__main__":
    main()
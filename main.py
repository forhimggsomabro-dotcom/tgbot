<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Digital Products Store</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Rajdhani:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://zapupi.com/single-html-web-kit.js"></script>

  <style>
    /* =========================================
       DIGITAL PRODUCTS STORE — PREMIUM CYBERPUNK UI
       ========================================= */
    :root {
      --bg: #f4f9ff;
      --card-solid: #ffffff;
      --card-glass: rgba(255,255,255,0.92);
      --signal: #1296db;
      --signal-hover: #0b7fc0;
      --signal-dim: rgba(212, 175, 55, 0.18);
      --line: rgba(212, 175, 55, 0.25);
      --line-soft: rgba(212, 175, 55, 0.12);
      --glow: rgba(212, 175, 55, 0.35);
      --amber: #FFD700;
      --red: #FF2A5F;
      --success: #00E65B;
      --success-hover: #00FF66;
      --text-hi: #12304a;
      --text-mid: #587084;
      --text-low: #7890a0;
      --mono: 'Rajdhani', sans-serif;
      --sans: 'Poppins', sans-serif;
      --radius: 12px;

      /* UI Element Variables for Theme Toggle */
      --header-bg: rgba(5, 5, 8, 0.8);
      --overlay-bg: rgba(3, 3, 5, 0.95);
      --modal-overlay: rgba(0,0,0,0.85);
      --sidebar-overlay: rgba(0,0,0,0.8);
      --input-bg: rgba(0,0,0,0.4);
      --box-bg: rgba(0,0,0,0.3);
      --badge-bg: rgba(0,0,0,0.5);
      --btn-text: #000000;
      --shadow-heavy: rgba(0,0,0,0.8);
      --shadow-mid: rgba(0,0,0,0.5);
      --shadow-low: rgba(0,0,0,0.3);
      --success-glow: rgba(0,230,91,0.3);
      --error-glow: rgba(255,42,95,0.3);
    }

    /* LIGHT THEME VARIABLES */
    body.light-theme {
      --bg: #F4F6F9;
      --card-solid: #FFFFFF;
      --card-glass: rgba(255, 255, 255, 0.85);
      --signal: #007ACC;
      --signal-hover: #005999;
      --signal-dim: rgba(0, 122, 204, 0.1);
      --line: rgba(0, 0, 0, 0.1);
      --line-soft: rgba(0, 0, 0, 0.05);
      --glow: rgba(0, 122, 204, 0.25);
      --amber: #D99C00;
      --red: #D32F2F;
      --success: #009944;
      --success-hover: #008033;
      --text-hi: #1A1A1A;
      --text-mid: #555555;
      --text-low: #777777;

      --header-bg: rgba(255, 255, 255, 0.85);
      --overlay-bg: rgba(244, 246, 249, 0.95);
      --modal-overlay: rgba(0,0,0,0.5);
      --sidebar-overlay: rgba(0,0,0,0.3);
      --input-bg: rgba(255,255,255,0.8);
      --box-bg: rgba(0,0,0,0.04);
      --badge-bg: rgba(0,0,0,0.06);
      --btn-text: #FFFFFF;
      --shadow-heavy: rgba(0,0,0,0.15);
      --shadow-mid: rgba(0,0,0,0.08);
      --shadow-low: rgba(0,0,0,0.05);
      --success-glow: rgba(0,153,68,0.2);
      --error-glow: rgba(211,47,47,0.2);
    }

    /* SMOOTH THEME TRANSITIONS */
    body, .header, .sidebar, .sidebar-overlay, .glass, .product-card, .btn, .modal-content, .input-group input, .search-box input, .data-item, .setting-item, .profile-card, .stat-box, .theme-toggle, .menu-item, .announcement, .loading-overlay {
      transition: background 0.3s ease, background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    
    body { font-family: var(--sans); background: linear-gradient(180deg,#ffffff,#eaf6ff); color: var(--text-mid); min-height: 100vh; }

    /* UTILITIES */
    .glass { background: var(--card-glass); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid var(--line); }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--glow); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--signal); }

    /* OVERLAYS & TOASTS */
    .loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--overlay-bg); backdrop-filter: blur(8px); z-index: 10000; display: none; align-items: center; justify-content: center; flex-direction: column; }
    .loading-overlay.active { display: flex; }
    .loading-spinner { width: 50px; height: 50px; border: 3px solid var(--line-soft); border-radius: 50%; border-top-color: var(--signal); animation: spin 1s linear infinite; margin-bottom: 15px; box-shadow: 0 0 15px var(--glow); }
    @keyframes spin { to { transform: rotate(360deg); } }
    
    .notification-toast { position: fixed; top: 80px; right: 16px; left: 16px; margin: 0 auto; max-width: 360px; background: var(--card-glass); backdrop-filter: blur(12px); border: 1px solid var(--line); border-left: 4px solid var(--signal); border-radius: var(--radius); padding: 14px 16px; color: var(--text-hi); font-size: 14px; font-family: var(--sans); z-index: 10001; display: none; animation: toastIn .4s cubic-bezier(.2,.9,.3,1.2); box-shadow: 0 12px 32px var(--shadow-heavy), 0 0 15px var(--glow); }
    @keyframes toastIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    .notification-toast.show { display: block; }
    .notification-toast.success { border-left-color: var(--success); box-shadow: 0 12px 32px var(--shadow-heavy), 0 0 15px var(--success-glow); }
    .notification-toast.error { border-left-color: var(--red); box-shadow: 0 12px 32px var(--shadow-heavy), 0 0 15px var(--error-glow); }

    /* HEADER */
    .header { background: var(--header-bg); backdrop-filter: blur(16px); border-bottom: 1px solid var(--line); padding: 14px 18px; position: sticky; top: 0; z-index: 1000; display: flex; align-items: center; justify-content: space-between; }
    .hamburger { width: 26px; height: 18px; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer; z-index: 1001; }
    .hamburger span { width: 100%; height: 2px; background: var(--text-hi); border-radius: 2px; transition: 0.3s; }
    .hamburger.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); background: var(--signal); }
    .hamburger.active span:nth-child(2) { opacity: 0; }
    .hamburger.active span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); background: var(--signal); }
    .brand-section { display: flex; align-items: center; gap: 10px; flex: 1; justify-content: center; }
    .brand-logo { width: 34px; height: 34px; border-radius: 8px; object-fit: cover; border: 1px solid var(--signal); box-shadow: 0 0 10px var(--glow); display:none; }
    .brand-name { font-family: var(--mono); font-size: 22px; font-weight: 800; color: var(--text-hi); text-transform: uppercase; letter-spacing: 1px; text-shadow: 0 0 10px var(--glow); }

    /* THEME TOGGLE BUTTON */
    .theme-toggle { background: transparent; border: 1px solid var(--line); color: var(--text-hi); width: 34px; height: 34px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: 10px; }
    .theme-toggle:hover { background: var(--signal-dim); border-color: var(--signal); color: var(--signal); box-shadow: 0 0 10px var(--glow); }

    /* SIDEBAR */
    .sidebar { position: fixed; top: 0; left: -300px; width: 280px; height: 100vh; background: var(--card-glass); backdrop-filter: blur(20px); border-right: 1px solid var(--line); padding: 80px 16px 20px; transition: left 0.4s ease; z-index: 999; overflow-y: auto; }
    .sidebar.active { left: 0; box-shadow: 10px 0 30px var(--shadow-heavy); }
    .sidebar-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: var(--sidebar-overlay); opacity: 0; visibility: hidden; transition: 0.4s; z-index: 998; }
    .sidebar-overlay.active { opacity: 1; visibility: visible; }
    .menu-item { padding: 14px 16px; margin-bottom: 8px; border-radius: 10px; cursor: pointer; transition: 0.3s; color: var(--text-mid); font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 14px; border: 1px solid transparent; }
    .menu-item:hover, .menu-item.active { background: var(--signal-dim); color: var(--text-hi); border-color: var(--line); transform: translateX(5px); }
    .menu-item i { color: var(--signal); width: 20px; text-align: center; text-shadow: 0 0 5px var(--glow); }

    /* MAIN CONTAINER */
    .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
    .section-title { font-family: var(--mono); font-size: 22px; color: var(--text-hi); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; font-weight: 800; border-bottom: 1px solid var(--line-soft); padding-bottom: 10px; }
    .section-title i { color: var(--signal); text-shadow: 0 0 8px var(--glow); }
    
    .tab-content { display: none; animation: fadeIn 0.4s ease; }
    .tab-content.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* SEARCH BAR */
    .search-box { position: relative; margin-bottom: 20px; }
    .search-box input { width: 100%; padding: 16px 20px 16px 50px; background: var(--input-bg); border: 1px solid var(--line); border-radius: 12px; color: var(--text-hi); font-size: 15px; font-family: var(--sans); transition: 0.3s; }
    .search-box input:focus { border-color: var(--signal); outline: none; box-shadow: 0 0 15px var(--glow); }
    .search-box i { position: absolute; left: 20px; top: 50%; transform: translateY(-50%); color: var(--signal); }

    /* ====================================================
       PRODUCTS GRID (Responsive Fix)
       ==================================================== */
    .products-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; margin-bottom: 40px; }
    
    .product-card { background: var(--card-glass); border: 1px solid var(--line); border-radius: var(--radius); padding: 15px; display: flex; flex-direction: column; transition: 0.3s; position: relative; overflow: hidden; }
    .product-card:hover { transform: translateY(-5px); border-color: var(--signal); box-shadow: 0 10px 25px var(--shadow-heavy), 0 0 15px var(--glow); }
    .product-image { width: 100%; height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; border: 1px solid var(--line-soft); background: var(--box-bg); }
    .product-title { font-size: 15px; font-weight: 700; color: var(--text-hi); margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4; word-break: break-word; }
    .product-price { font-family: var(--mono); font-size: 20px; font-weight: 800; color: var(--signal); margin-bottom: 15px; text-shadow: 0 0 8px var(--glow); }
    
    /* margin-top: auto pushes the actions block securely to the bottom, ensuring cards keep equal height gracefully */
    .product-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-top: auto; width: 100%; }
    
    /* 
       --- CRITICAL RESPONSIVE GRID FIX ---
       Fixed the Tablet breakpoint from `max-width: 1024px` back to `max-width: 979px`.
       Reason: Chrome Android's "Request Desktop Site" inherently forces a 980px viewport simulation. 
       At 1024px, the 980px desktop view fell under the tablet rules and restricted to 3 columns.
       By setting the tablet max-width to 979px, 980px correctly utilizes the 4-column desktop layout.
    */
    @media (max-width: 979px) {
      .products-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 15px; }
    }

    @media (max-width: 768px) {
      .products-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
      .product-card { padding: 12px; border-radius: 10px; }
      .product-image { height: 110px; margin-bottom: 10px; }
      .product-title { font-size: 13px; line-height: 1.4; margin-bottom: 6px; }
      .product-price { font-size: 15px; margin-bottom: 10px; }
      .product-actions { grid-template-columns: minmax(0, 1fr); gap: 6px; }
      .btn { padding: 8px; font-size: 12px; border-radius: 8px; }
    }
    /* ==================================================== */

    /* BUTTONS */
    .btn { padding: 12px 16px; background: var(--signal); border: 1px solid var(--signal); border-radius: 10px; color: var(--btn-text); font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.3s; text-align: center; font-family: var(--sans); box-shadow: 0 0 10px var(--glow); display: flex; align-items: center; justify-content: center; gap: 8px; }
    .btn:hover:not(:disabled) { background: var(--signal-hover); transform: translateY(-2px); box-shadow: 0 0 20px var(--glow); }
    .btn-secondary { background: var(--signal-dim); color: var(--signal); border-color: var(--line); box-shadow: none; }
    .btn-secondary:hover:not(:disabled) { background: var(--glow); color: var(--text-hi); }
    .btn-free { background: var(--success); border-color: var(--success); box-shadow: 0 0 10px var(--success-glow); color: var(--btn-text); }
    .btn-free:hover:not(:disabled) { background: var(--success-hover); box-shadow: 0 0 20px var(--success-glow); }

    /* HOME PROFILE CARD */
    .profile-card { background: var(--card-glass); border: 1px solid var(--line); border-radius: var(--radius); padding: 25px; display: flex; gap: 20px; align-items: center; margin-bottom: 30px; flex-wrap: wrap; box-shadow: 0 10px 30px var(--shadow-mid); }
    .profile-avatar { width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--signal); box-shadow: 0 0 15px var(--glow); background: var(--signal-dim); display: flex; align-items: center; justify-content: center; font-size: 32px; color: var(--signal); font-family: var(--mono); font-weight: 800; text-transform: uppercase; }
    .profile-stats { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px; width: 100%; border-top: 1px solid var(--line-soft); padding-top: 15px; }
    .stat-box { flex: 1; min-width: 100px; background: var(--box-bg); border: 1px solid var(--line-soft); border-radius: 10px; padding: 15px; text-align: center; }
    .stat-value { font-family: var(--mono); font-size: 24px; font-weight: 800; color: var(--signal); text-shadow: 0 0 10px var(--glow); }
    .stat-label { font-size: 11px; color: var(--text-mid); text-transform: uppercase; font-weight: 600; margin-top: 5px; }

    /* BANNER & ANNOUNCEMENT */
    .store-banner { width: 100%; height: 200px; object-fit: cover; border-radius: var(--radius); border: 1px solid var(--line); margin-bottom: 20px; box-shadow: 0 0 20px var(--glow); display: none; }
    .announcement { background: var(--signal-dim); border: 1px solid var(--signal); border-radius: 10px; padding: 15px 20px; color: var(--text-hi); font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; box-shadow: inset 0 0 15px var(--glow); display: none; }
    
    /* TABLES / LISTS */
    .data-list { display: flex; flex-direction: column; gap: 15px; }
    .data-item { background: var(--card-glass); border: 1px solid var(--line); border-radius: 12px; padding: 15px; display: flex; gap: 15px; align-items: center; transition: 0.3s; flex-wrap: wrap; }
    .data-item:hover { border-color: var(--signal); box-shadow: 0 0 15px var(--glow); }
    .data-img { width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid var(--line-soft); }

    /* MODALS */
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--modal-overlay); backdrop-filter: blur(10px); z-index: 2000; align-items: center; justify-content: center; padding: 15px; }
    .modal.active { display: flex; animation: fadeIn 0.3s ease; }
    .modal-content { background: var(--card-solid); border: 1px solid var(--line); border-radius: 16px; padding: 25px; width: 100%; max-width: 600px; max-height: 90vh; overflow-y: auto; position: relative; box-shadow: 0 0 30px var(--glow); }
    .modal-close { position: absolute; top: 15px; right: 15px; width: 35px; height: 35px; background: var(--box-bg); border: 1px solid var(--line); border-radius: 8px; color: var(--text-hi); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.3s; }
    .modal-close:hover { background: var(--red); border-color: var(--red); box-shadow: 0 0 10px var(--red); color: #fff; }
    .input-group { margin-bottom: 15px; }
    .input-group label { display: block; margin-bottom: 8px; font-size: 13px; color: var(--text-mid); text-transform: uppercase; font-weight: 600; }
    .input-group input { width: 100%; padding: 14px; background: var(--input-bg); border: 1px solid var(--line); border-radius: 10px; color: var(--text-hi); font-family: var(--sans); }
    .input-group input:focus { border-color: var(--signal); outline: none; box-shadow: 0 0 10px var(--glow); }

    .about-gallery { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; margin: 15px 0; }
    .about-gallery img { height: 80px; border-radius: 8px; border: 1px solid var(--line); cursor: pointer; transition: 0.3s; }
    .about-gallery img:hover { border-color: var(--signal); box-shadow: 0 0 10px var(--glow); }

    .empty-state { text-align: center; padding: 60px 20px; color: var(--text-mid); grid-column: 1 / -1; }
    .empty-state i { font-size: 50px; color: var(--signal); opacity: 0.5; margin-bottom: 15px; }

    /* SETTINGS UI */
    .setting-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; background: var(--card-glass); border: 1px solid var(--line); border-radius: 12px; margin-bottom: 15px; }
  
/* White Light Blue Premium UI */
.announcement {
  overflow:hidden !important;
  white-space:nowrap;
}
.announcement span {
  display:inline-block;
  animation: movingNotice 12s linear infinite;
}
@keyframes movingNotice {
 from { transform:translateX(100%); }
 to { transform:translateX(-100%); }
}
.why-section {
 background:white;
 border:1px solid #d8ebf8;
 border-radius:18px;
 padding:25px;
 margin-bottom:30px;
 box-shadow:0 8px 25px rgba(18,150,219,.12);
}
.why-grid {
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:15px;
}
.why-card {
 background:#f4faff;
 border:1px solid #d8ebf8;
 border-radius:14px;
 padding:20px;
 text-align:center;
}
.why-card i {
 color:#1296db;
 font-size:28px;
 margin-bottom:10px;
}
.why-card h3 {
 color:#12304a;
 margin-bottom:8px;
}
.why-card p {
 color:#587084;
 font-size:14px;
}
.browse-btn {
 margin:25px auto 0;
 max-width:260px;
}
@media(max-width:768px){
 .why-grid{grid-template-columns:1fr;}
}

</style>
</head>
<body>

  <!-- Loaders & Overlays -->
  <div class="loading-overlay" id="loadingOverlay">
    <div class="loading-spinner"></div>
    <div style="color:var(--signal); font-family:var(--mono); font-size:16px; font-weight:700; letter-spacing:2px;" id="loadingText">SYNCING...</div>
  </div>
  <div class="notification-toast" id="notificationToast"></div>

  <!-- Header -->
  <div class="header">
    <div class="hamburger" id="hamburger" onclick="toggleSidebar()">
      <span></span><span></span><span></span>
    </div>
    <div class="brand-section">
      <img id="headerLogo" class="brand-logo" src="">
      <div id="headerBrandName" class="brand-name">MACRO VIP STORE</div>
      <!-- Theme Toggle Button -->
      <button id="themeToggleBtn" onclick="toggleTheme()" class="theme-toggle" aria-label="Toggle Theme">
        <i class="fas fa-moon"></i>
      </button>
    </div>
    <div style="width: 26px;"></div> <!-- Spacer for centering -->
  </div>

  <!-- Sidebar -->
  <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
  <div class="sidebar" id="sidebar">
    <div class="menu-item active" data-tab="home"><i class="fas fa-home"></i> Home</div>
    <div class="menu-item" data-tab="paid"><i class="fas fa-gem"></i> Premium Products</div>
    <div class="menu-item" data-tab="free"><i class="fas fa-gift"></i> Free Downloads</div>
    
    <div id="authMenuSection" style="display:none;">
      <div style="margin: 20px 0 10px; font-size: 11px; color: var(--text-mid); text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">My Account</div>
      <div class="menu-item" data-tab="orders"><i class="fas fa-box"></i> My Library</div>
      <div class="menu-item" data-tab="history"><i class="fas fa-history"></i> Purchase History</div>
    </div>

    <div style="margin: 20px 0 10px; font-size: 11px; color: var(--text-mid); text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">Support & Legal</div>
    <div class="menu-item" data-tab="contact"><i class="fas fa-headset"></i> Contact Us</div>
    <div class="menu-item" data-tab="terms"><i class="fas fa-file-contract"></i> Terms & Conditions</div>
    <div class="menu-item" data-tab="privacy"><i class="fas fa-user-shield"></i> Privacy Policy</div>
    <div class="menu-item" data-tab="refund"><i class="fas fa-undo"></i> Refund Policy</div>
    
    <div style="margin: 20px 0 10px; font-size: 11px; color: var(--text-mid); text-transform: uppercase; font-weight: 800; letter-spacing: 1px;">System</div>
    <div class="menu-item" data-tab="settings"><i class="fas fa-cog"></i> Settings</div>
    
    <div id="logoutBtn" class="menu-item" style="color:var(--red); display:none;" onclick="logoutUser()"><i class="fas fa-power-off" style="color:var(--red);"></i> Logout</div>
    <div id="loginBtn" class="menu-item" style="color:var(--success);" onclick="showAuthModal()"><i class="fas fa-sign-in-alt" style="color:var(--success);"></i> Login / Register</div>
  </div>

  <!-- MAIN CONTENT CONTAINER -->
  <div class="container">
    
    <!-- HOME TAB -->
    <div id="homeTab" class="tab-content active">
      <div id="announcementBar" class="announcement"><i class="fas fa-bullhorn"></i> <span id="announcementText"></span></div>
      <img id="storeBanner" class="store-banner" src="">

      <div id="profileCard" class="profile-card" style="display:none;">
        <div class="profile-avatar" id="profileAvatar">U</div>
        <div style="flex:1;">
          <h2 style="color:var(--text-hi); font-size:22px;" id="profileName">User Name</h2>
          <p style="color:var(--text-mid); font-size:14px;" id="profileEmail">user@email.com</p>
          <p style="color:var(--text-low); font-size:12px; margin-top:5px;">Joined: <span id="profileJoined"></span></p>
        </div>
        <div class="profile-stats">
          <div class="stat-box"><div class="stat-value" id="statPurchased">0</div><div class="stat-label">Purchased</div></div>
          <div class="stat-box"><div class="stat-value" id="statFree">0</div><div class="stat-label">Downloaded</div></div>
          <div class="stat-box"><div class="stat-value" id="statOrders">0</div><div class="stat-label">Total Library</div></div>
        </div>
      </div>

      <div id="welcomeMessage" style="text-align:center; padding: 40px 20px; background:var(--card-glass); border-radius:var(--radius); border:1px solid var(--line); margin-bottom:30px;">
        <h1 style="color:var(--signal); font-family:var(--mono); font-size:28px; margin-bottom:10px; text-transform:uppercase;">WELCOME TO PREMIUM DIGITAL STORE</h1>
        <p style="color:var(--text-mid);">Explore premium digital services with a simple and secure experience. <a href="#" onclick="showAuthModal()" style="color:var(--signal);">Login</a> to access your dashboard.</p>
      </div>

      <div class="why-section">
        <h2 class="section-title"><i class="fas fa-star"></i> Why Choose Us</h2>
        <div class="why-grid">
          <div class="why-card"><i class="fas fa-shield-alt"></i><h3>Trusted Service</h3><p>Clear information and reliable support.</p></div>
          <div class="why-card"><i class="fas fa-bolt"></i><h3>Fast Access</h3><p>Quick delivery after successful purchase.</p></div>
          <div class="why-card"><i class="fas fa-headset"></i><h3>Support</h3><p>Help available whenever you need it.</p></div>
        </div>
        <button class="btn browse-btn" onclick="document.querySelector('[data-tab=paid]').click()">Browse Products</button>
      </div>
      <h2 class="section-title"><i class="fas fa-bolt"></i> Latest Arrivals</h2>
      <div id="homeLatestGrid" class="products-grid"></div>
    </div>

    <!-- PAID PRODUCTS TAB -->
    <div id="paidTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-gem"></i> Premium Products</h2>
      <div class="search-box"><i class="fas fa-search"></i><input type="text" id="searchPaid" placeholder="Search premium products..." oninput="filterProducts('paid')"></div>
      <div id="paidGrid" class="products-grid"></div>
    </div>

    <!-- FREE PRODUCTS TAB -->
    <div id="freeTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-gift"></i> Free Downloads</h2>
      <div class="search-box"><i class="fas fa-search"></i><input type="text" id="searchFree" placeholder="Search free products..." oninput="filterProducts('free')"></div>
      <div id="freeGrid" class="products-grid"></div>
    </div>

    <!-- MY ORDERS TAB -->
    <div id="ordersTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-box"></i> My Library</h2>
      <div class="search-box"><i class="fas fa-search"></i><input type="text" id="searchOrders" placeholder="Search my library..." oninput="renderOrders()"></div>
      <div id="ordersList" class="data-list"></div>
    </div>

    <!-- PURCHASE HISTORY TAB -->
    <div id="historyTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-history"></i> Purchase History</h2>
      <div class="search-box"><i class="fas fa-search"></i><input type="text" id="searchHistory" placeholder="Search transactions..." oninput="renderHistory()"></div>
      <div id="historyList" class="data-list"></div>
    </div>

    <!-- CONTACT US TAB -->
    <div id="contactTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-headset"></i> Support Channels</h2>
      <div id="contactGrid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(300px,1fr)); gap:15px;"></div>
    </div>

    <!-- POLICIES TABS -->
    <div id="termsTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-file-contract"></i> Terms & Conditions</h2>
      <div id="termsContent" style="background:var(--card-glass); padding:20px; border-radius:12px; border:1px solid var(--line); line-height:1.6; color: var(--text-hi);"></div>
    </div>
    <div id="privacyTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-user-shield"></i> Privacy Policy</h2>
      <div id="privacyContent" style="background:var(--card-glass); padding:20px; border-radius:12px; border:1px solid var(--line); line-height:1.6; color: var(--text-hi);"></div>
    </div>
    <div id="refundTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-undo"></i> Refund Policy</h2>
      <div id="refundContent" style="background:var(--card-glass); padding:20px; border-radius:12px; border:1px solid var(--line); line-height:1.6; color: var(--text-hi);"></div>
    </div>

    <!-- SETTINGS TAB -->
    <div id="settingsTab" class="tab-content">
      <h2 class="section-title"><i class="fas fa-cog"></i> App Settings</h2>
      
      <!-- Account Settings Block (Shown Only if Logged In) -->
      <div id="accountSettingsBlock" style="display:none;">
        <h3 style="color:var(--signal); margin: 30px 0 15px; font-family:var(--mono); text-transform:uppercase;">Account Settings</h3>
        
        <div class="setting-item" style="flex-direction:column; align-items:stretch; gap:10px;">
          <div><strong>Change Username</strong><br><span style="font-size:12px;color:var(--text-mid);">Update your display name</span></div>
          <div class="input-group" style="margin-bottom:0;"><input type="text" id="settingCurrentName" readonly style="opacity:0.6; pointer-events:none;"></div>
          <div class="input-group" style="margin-bottom:0;"><input type="text" id="settingNewName" placeholder="New Username"></div>
          <button class="btn btn-secondary" onclick="updateUsername()">Save Username</button>
        </div>

        <div class="setting-item" style="flex-direction:column; align-items:stretch; gap:10px;">
          <div><strong>Change Password</strong><br><span style="font-size:12px;color:var(--text-mid);">Secure your account</span></div>
          <div class="input-group" style="margin-bottom:0;"><input type="password" id="settingCurrentPassword" placeholder="Current Password"></div>
          <div class="input-group" style="margin-bottom:0;"><input type="password" id="settingNewPassword" placeholder="New Password"></div>
          <div class="input-group" style="margin-bottom:0;"><input type="password" id="settingConfirmPassword" placeholder="Confirm New Password"></div>
          <button class="btn btn-secondary" onclick="updatePassword()">Update Password</button>
        </div>
      </div>

      <h3 style="color:var(--signal); margin: 30px 0 15px; font-family:var(--mono); text-transform:uppercase;">System Data</h3>
      <div class="setting-item">
        <div><strong>App Version</strong><br><span style="font-size:12px;color:var(--text-mid);">v5.0.0 Cyberpunk Edition</span></div>
      </div>
      <div class="setting-item">
        <div><strong>Clear Local Cache</strong><br><span style="font-size:12px;color:var(--text-mid);">Fixes loading issues</span></div>
        <button class="btn btn-secondary" style="padding:8px 15px;" onclick="localStorage.clear(); showNotification('Cache Cleared! Reloading...'); setTimeout(()=>location.reload(),1000);">Clear</button>
      </div>
    </div>

  </div> <!-- End Container -->

  <!-- MODALS -->

  <!-- Auth Modal -->
  <div id="authModal" class="modal">
    <div class="modal-content" style="max-width: 400px;">
      <span class="modal-close" onclick="closeModal('authModal')">×</span>
      <h2 class="section-title" id="authTitle" style="border:none; justify-content:center;"><i class="fas fa-fingerprint"></i>Login</h2>
      
      <div id="loginForm">
        <div class="input-group"><label>Email</label><input type="email" id="loginEmail" placeholder="Enter Your Email"></div>
        <div class="input-group"><label>Password</label><input type="password" id="loginPassword" placeholder="••••••••"></div>
        <button class="btn" style="width:100%;" onclick="loginUser()">Login</button>
        <p style="text-align:center; margin-top:20px; font-size:13px;">New user? <a href="#" style="color:var(--signal);" onclick="toggleAuthMode('signup')">Create Account</a></p>
      </div>

      <div id="signupForm" style="display:none;">
        <div class="input-group"><label>Username</label><input type="text" id="signupName" placeholder="Enter Your Name"></div>
        <div class="input-group"><label>Email</label><input type="email" id="signupEmail" placeholder="Enter Your Email"></div>
        <div class="input-group"><label>Password</label><input type="password" id="signupPassword" placeholder="••••••••"></div>
        <button class="btn" style="width:100%;" onclick="signupUser()">Register</button>
        <p style="text-align:center; margin-top:20px; font-size:13px;">Already have an account? <a href="#" style="color:var(--signal);" onclick="toggleAuthMode('login')">Login</a></p>
      </div>
    </div>
  </div>

  <!-- Product About Modal -->
  <div id="aboutModal" class="modal">
    <div class="modal-content" style="max-width: 700px;">
      <span class="modal-close" onclick="closeModal('aboutModal')">×</span>
      <div style="display:flex; gap:20px; flex-wrap:wrap; margin-bottom:20px; align-items:flex-start;">
        <img id="aboutImage" src="" style="width:120px; height:120px; object-fit:cover; border-radius:12px; border:1px solid var(--signal); box-shadow:0 0 15px var(--glow);">
        <div style="flex:1;">
          <h2 id="aboutTitle" style="font-size:24px; color:var(--text-hi); margin-bottom:10px;"></h2>
          <div id="aboutPrice" style="font-family:var(--mono); font-size:28px; font-weight:800; color:var(--signal); text-shadow:0 0 10px var(--glow); margin-bottom:10px;"></div>
          <div style="display:flex; gap:10px; font-size:12px; color:var(--text-mid); flex-wrap:wrap;">
            <span style="background:var(--badge-bg); padding:4px 8px; border-radius:6px; border:1px solid var(--line);"><i class="fas fa-tag"></i> <span id="aboutCategory"></span></span>
            <span style="background:var(--badge-bg); padding:4px 8px; border-radius:6px; border:1px solid var(--line);"><i class="fas fa-code-branch"></i> v<span id="aboutVersion"></span></span>
          </div>
        </div>
      </div>
      
      <div id="aboutGallery" class="about-gallery"></div>
      
      <h3 style="color:var(--signal); font-family:var(--mono); margin-bottom:10px; text-transform:uppercase;">Description</h3>
      <div id="aboutDesc" style="color:var(--text-hi); line-height:1.6; font-size:14px; margin-bottom:20px; background:var(--box-bg); padding:15px; border-radius:10px; border:1px solid var(--line-soft);"></div>
      
      <div id="aboutActionBtn"></div>
    </div>
  </div>

  <!-- Success / Download Modal -->
  <div id="successModal" class="modal">
    <div class="modal-content" style="max-width: 500px; text-align:center;">
      <span class="modal-close" onclick="closeModal('successModal')">×</span>
      <i class="fas fa-check-circle" style="font-size:60px; color:var(--success); text-shadow: 0 0 20px var(--success-glow); margin-bottom:20px;"></i>
      <h2 style="color:var(--text-hi); margin-bottom:10px;">Access Granted!</h2>
      <p style="color:var(--text-mid); margin-bottom:25px;" id="successMsg">Your product is ready.</p>
      
      <input type="text" id="successLinkInput" readonly style="width:100%; padding:12px; background:var(--input-bg); border:1px solid var(--line); border-radius:8px; color:var(--signal); margin-bottom:20px; text-align:center;">
      
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        <button class="btn btn-secondary" onclick="copySuccessLink()"><i class="fas fa-copy"></i> Copy Link</button>
        <button class="btn btn-free" id="successOpenBtn"><i class="fas fa-external-link-alt"></i> Open Link</button>
      </div>
    </div>
  </div>

  <!-- FIREBASE SCRIPTS -->
  <script type="module">
    import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js';
    import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged, updateProfile, updatePassword, reauthenticateWithCredential, EmailAuthProvider } from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js';
    import { getDatabase, ref, get, set, push, onValue, remove } from 'https://www.gstatic.com/firebasejs/9.22.1/firebase-database.js';

    // FIREBASE CONFIGURATION
const firebaseConfig = {
  apiKey: "AIzaSyB2QGFe05gaNUQjpC4LmoW-A6yJe5hgkvo",
  authDomain: "aiservice-e286d.firebaseapp.com",
  databaseURL: "https://aiservice-e286d-default-rtdb.firebaseio.com",
  projectId: "aiservice-e286d",
  storageBucket: "aiservice-e286d.firebasestorage.app",
  messagingSenderId: "527132045853",
  appId: "1:527132045853:web:70e64276e03fd93abf0cf4",
  measurementId: "G-F4T3XQM19T"
};

// INITIALIZE FIREBASE
const app = initializeApp(firebaseConfig);

window.auth = getAuth(app);
window.db = getDatabase(app);

// AUTH HELPERS
window.authSignIn = signInWithEmailAndPassword;
window.authSignUp = createUserWithEmailAndPassword;
window.authSignOut = signOut;
window.authUpdate = updateProfile;
window.authUpdatePassword = updatePassword;
window.reauthenticateWithCredential = reauthenticateWithCredential;
window.EmailAuthProvider = EmailAuthProvider;

// DATABASE HELPERS
window.dbRef = ref;
window.dbGet = get;
window.dbSet = set;
window.dbPush = push;
window.dbRemove = remove;
    // GLOBAL STATE
    window.currentUser = null;
    window.allProducts = [];
    window.allOrders = [];
    window.allPayments = [];
    window.pgSettings = {};
    window.storeCurrency = '$';

    function initDataListeners() {
      showLoading('LOADING STORE...');
      
      // General Settings
      onValue(ref(window.db, 'settings/general'), s => {
        if(s.exists()){
          const d = s.val();
          window.storeCurrency = d.currency || '$';
          if(d.siteName) document.getElementById('headerBrandName').innerText = d.siteName;
          if(d.logo) { document.getElementById('headerLogo').src = d.logo; document.getElementById('headerLogo').style.display = 'block'; }
          if(d.storeBanner) { document.getElementById('storeBanner').src = d.storeBanner; document.getElementById('storeBanner').style.display = 'block'; }
          if(d.announcementBar) { document.getElementById('announcementText').innerText = d.announcementBar; document.getElementById('announcementBar').style.display = 'flex'; }
        }
      });

      // Gateway Settings (Linked safely from the Admin setup node)
      onValue(ref(window.db, 'settings/payment'), s => { if(s.exists()) window.pgSettings = s.val(); });

      // Dynamic CMS Pages (Fixed to match Admin CMS hierarchy)
      const pages = ['terms','privacy','refund'];
      pages.forEach(p => {
        onValue(ref(window.db, `cms/${p}`), s => { 
          document.getElementById(`${p}Content`).innerHTML = s.exists() ? s.val().content : '<div class="empty-state"><i class="fas fa-file-alt"></i><br><h3>Content not published yet.</h3></div>'; 
        });
      });

      // Unified Products Realtime Parser (handles Free, Paid & Legacy)
      onValue(ref(window.db, 'products'), s => {
        window.allProducts = [];
        if(s.exists()){
          const val = s.val();
          
          // Parse Paid Products
          if (val.paid) {
            Object.entries(val.paid).forEach(([id, p]) => {
              if(p.status !== 'hidden') window.allProducts.push({id, type: 'paid', ...p});
            });
          }
          
          // Parse Free Products
          if (val.free) {
            Object.entries(val.free).forEach(([id, p]) => {
              if(p.status !== 'hidden') window.allProducts.push({id, type: 'free', ...p});
            });
          }
          
          // Parse Legacy (flat products) safety fallback
          Object.keys(val).forEach(k => {
            if (k !== 'paid' && k !== 'free' && typeof val[k] === 'object') {
               const p = val[k];
               if(p.status !== 'hidden') {
                 const legacyType = (p.price && parseFloat(p.price) > 0) ? 'paid' : 'free';
                 window.allProducts.push({id: k, type: legacyType, legacy: true, ...p});
               }
            }
          });
          
          window.allProducts.sort((a,b) => (b.displayOrder||0) - (a.displayOrder||0));
        }
        renderProducts(); hideLoading();
      });

      // Contact Links
      onValue(ref(window.db, 'supportLinks'), s => {
        const cg = document.getElementById('contactGrid'); cg.innerHTML = '';
        if(s.exists()){
          Object.values(s.val()).forEach(l => {
            cg.innerHTML += `
              <div class="product-card" style="flex-direction:row; align-items:center; gap:15px; padding:20px;">
                <img src="${escapeHtml(l.logo)}" style="width:50px;height:50px;object-fit:cover;border-radius:10px;border:1px solid var(--signal);" onerror="this.src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='">
                <div style="flex:1;">
                  <h3 style="color:var(--text-hi); font-size:16px;">${escapeHtml(l.name)}</h3>
                </div>
                <button class="btn btn-secondary" onclick="window.open('${escapeHtml(l.link)}','_blank')">Open</button>
              </div>
            `;
          });
        }
      });
    }

    onAuthStateChanged(window.auth, (user) => {
      window.currentUser = user;
      updateAuthUI();
      if(user) {
        // Load User Orders & Payments
        onValue(ref(window.db, 'orders'), async s => {
          window.allOrders = [];
          if(s.exists()){
            Object.entries(s.val()).forEach(([id,o])=>{ if(o.userId === user.uid) window.allOrders.push({id,...o}); });
            window.allOrders.sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt));
          }
          renderOrders(); updateProfileStats(); renderProducts(); // Re-render to update Owned buttons
        });
        onValue(ref(window.db, 'payments'), s => {
          window.allPayments = [];
          if(s.exists()){
            Object.entries(s.val()).forEach(([id,p])=>{ if(p.uid === user.uid) window.allPayments.push({id,...p}); });
            window.allPayments.sort((a,b)=>new Date(b.date)-new Date(a.date));
          }
          renderHistory();
        });
      } else {
        window.allOrders = [];
        window.allPayments = [];
        renderProducts(); // Re-render for logged out state
      }
    });

    initDataListeners();
  </script>

  <!-- UI & INTERACTION LOGIC -->
  <script>
    // Theme logic
    document.addEventListener('DOMContentLoaded', () => {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        const icon = document.querySelector('#themeToggleBtn i');
        if (icon) icon.className = 'fas fa-sun';
      }
    });

    function toggleTheme() {
      const body = document.body;
      const isLight = body.classList.toggle('light-theme');
      const icon = document.querySelector('#themeToggleBtn i');
      
      if (isLight) {
        icon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'light');
      } else {
        icon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'dark');
      }
    }

    function showLoading(txt) { document.getElementById('loadingText').innerText=txt; document.getElementById('loadingOverlay').classList.add('active'); }
    function hideLoading() { document.getElementById('loadingOverlay').classList.remove('active'); }
    function showNotification(m, t='success') { const n = document.getElementById('notificationToast'); n.textContent=m; n.className=`notification-toast show ${t}`; setTimeout(()=>n.classList.remove('show'), 3000); }
    function closeModal(id) { document.getElementById(id).classList.remove('active'); }
    function escapeHtml(t) { if(!t)return''; const d=document.createElement('div');d.textContent=t;return d.innerHTML; }
    function formatCurrency(a) { return (window.storeCurrency||'$') + parseFloat(a||0).toLocaleString('en-IN',{maximumFractionDigits:2}); }

    // Sidebar & Navigation
    function toggleSidebar() { document.getElementById('sidebar').classList.toggle('active'); document.getElementById('sidebarOverlay').classList.toggle('active'); document.getElementById('hamburger').classList.toggle('active'); }
    
    // Fixed: Switched from inline override to event listeners so HTML functions execute cleanly
    document.querySelectorAll('.menu-item').forEach(el => {
      el.addEventListener('click', function() {
        if(this.id==='logoutBtn' || this.id==='loginBtn') {
          if(window.innerWidth<=768) toggleSidebar();
          return;
        }
        document.querySelectorAll('.menu-item').forEach(i=>i.classList.remove('active')); this.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
        document.getElementById(this.dataset.tab+'Tab').classList.add('active');
        if(window.innerWidth<=768) toggleSidebar();
        window.scrollTo(0,0);
      });
    });

    // Verify ownership safely
    function hasPurchased(productId) {
      if(!window.currentUser || !window.allOrders) return false;
      return window.allOrders.some(o => o.productId === productId && (o.status === 'confirmed' || o.status === 'paid' || o.status === 'delivered'));
    }

    // Auth UI
    function showAuthModal() { closeModal('successModal'); closeModal('aboutModal'); toggleAuthMode('login'); document.getElementById('authModal').classList.add('active'); }
    function toggleAuthMode(m) {
      document.getElementById('loginForm').style.display = m==='login'?'block':'none';
      document.getElementById('signupForm').style.display = m==='signup'?'block':'none';
      document.getElementById('authTitle').innerHTML = m === 'login' ? '<i class="fas fa-fingerprint"></i>Login' : '<i class="fas fa-fingerprint"></i>Register';
    }
    
    function updateAuthUI() {
      const u = window.currentUser;
      document.getElementById('loginBtn').style.display = u?'none':'flex';
      document.getElementById('logoutBtn').style.display = u?'flex':'none';
      document.getElementById('authMenuSection').style.display = u?'block':'none';
      document.getElementById('accountSettingsBlock').style.display = u?'block':'none';
      
      const pc = document.getElementById('profileCard');
      const wm = document.getElementById('welcomeMessage');
      if(u) {
        pc.style.display = 'flex'; wm.style.display = 'none';
        const dName = u.displayName || 'User';
        document.getElementById('profileAvatar').innerText = dName.charAt(0).toUpperCase();
        document.getElementById('profileName').innerText = dName;
        document.getElementById('profileEmail').innerText = u.email;
        document.getElementById('profileJoined').innerText = u.metadata.creationTime ? new Date(u.metadata.creationTime).toLocaleDateString() : 'N/A';
        document.getElementById('settingCurrentName').value = dName;
      } else {
        pc.style.display = 'none'; wm.style.display = 'block';
      }
    }

    async function loginUser() {
      const e=document.getElementById('loginEmail').value, p=document.getElementById('loginPassword').value;
      if(!e||!p) return showNotification('Enter credentials','error');
      showLoading('AUTHENTICATING...');
      try { await window.authSignIn(window.auth, e, p); closeModal('authModal'); showNotification('Welcome Back!'); }
      catch(er){ showNotification(er.message,'error'); } finally{ hideLoading(); }
    }
    
    async function signupUser() {
      const n=document.getElementById('signupName').value.trim(), e=document.getElementById('signupEmail').value, p=document.getElementById('signupPassword').value;
      if(!n||!e||!p) return showNotification('Fill all fields','error');
      showLoading('CREATING ACCOUNT...');
      try {
        const c = await window.authSignUp(window.auth, e, p);
        await window.authUpdate(c.user, {displayName:n});
        closeModal('authModal'); showNotification('Account Created!');
      } catch(er){ showNotification(er.message,'error'); } finally { hideLoading(); }
    }
    
    // Fixed: Complete purge mechanism with seamless visual fallback & immediate UI response
    async function logoutUser() { 
      showLoading('LOGGING OUT...'); 
      try {
        // Sign out Firebase Session
        await window.authSignOut(window.auth); 
        
        // Deep Clean Browser Sessions
        localStorage.clear();
        sessionStorage.clear();
        
        // Restore Theme Preference since localStorage was cleared
        const isLight = document.body.classList.contains('light-theme');
        if (isLight) localStorage.setItem('theme', 'light');
        else localStorage.setItem('theme', 'dark');

        // Purge memory parameters
        window.currentUser = null;
        window.allOrders = [];
        window.allPayments = [];
        
        // Visually update the frontend without waiting for a reload 
        updateAuthUI();
        renderProducts();
        
        // Fallback to Home Tab instantly masking restricted pages
        document.querySelectorAll('.menu-item').forEach(i=>i.classList.remove('active'));
        document.querySelector('[data-tab="home"]').classList.add('active');
        document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
        document.getElementById('homeTab').classList.add('active');
        
        hideLoading();
        showNotification('Logged out successfully!', 'success');
        
        // Safe refresh to terminate memory leaks/active DB connections (Slight delay for user visual confirmation)
        setTimeout(() => {
          window.location.reload(); 
        }, 500); 
      } catch(e) { 
        hideLoading(); 
        showNotification(e.message, 'error'); 
      } 
    }

    function updateProfileStats() {
      if(!window.currentUser) return;
      let paid = 0, free = 0;
      window.allOrders.forEach(o => {
        if(o.status==='confirmed' || o.status==='paid' || o.status==='delivered') {
          if(parseFloat(o.finalAmount||0)>0) paid++; else free++;
        }
      });
      document.getElementById('statPurchased').innerText = paid;
      document.getElementById('statFree').innerText = free;
      document.getElementById('statOrders').innerText = window.allOrders.length;
    }

    // Account Settings - Update Username
    window.updateUsername = async () => {
      if(!window.currentUser) return;
      const newName = document.getElementById('settingNewName').value.trim();
      if(!newName) return showNotification('Please enter a new username', 'error');
      
      showLoading('UPDATING PROFILE...');
      try {
        await window.authUpdate(window.currentUser, { displayName: newName });
        updateAuthUI();
        document.getElementById('settingNewName').value = '';
        showNotification('Username updated successfully!');
      } catch(e) {
        showNotification(e.message, 'error');
      } finally { hideLoading(); }
    };

    // Account Settings - Update Password
    window.updatePassword = async () => {
      if(!window.currentUser) return;
      const curPass = document.getElementById('settingCurrentPassword').value;
      const newPass = document.getElementById('settingNewPassword').value;
      const confPass = document.getElementById('settingConfirmPassword').value;
      
      if(!curPass || !newPass || !confPass) return showNotification('Fill all password fields', 'error');
      if(newPass !== confPass) return showNotification('New passwords do not match', 'error');
      if(newPass.length < 8) return showNotification('Password must be at least 8 characters', 'error');

      showLoading('VERIFYING & UPDATING...');
      try {
        const cred = window.EmailAuthProvider.credential(window.currentUser.email, curPass);
        await window.reauthenticateWithCredential(window.currentUser, cred);
        await window.authUpdatePassword(window.currentUser, newPass);
        
        document.getElementById('settingCurrentPassword').value = '';
        document.getElementById('settingNewPassword').value = '';
        document.getElementById('settingConfirmPassword').value = '';
        showNotification('Password updated successfully!');
      } catch(e) {
        showNotification(e.message, 'error');
      } finally { hideLoading(); }
    };

    // Products Rendering Logic
    function getCardHTML(p) {
      const isFree = p.type === 'free' || (!p.price || parseFloat(p.price) === 0);
      const isOwned = hasPurchased(p.id);
      
      let bBtn = '';
      if(isOwned) {
        bBtn = `<button class="btn btn-free" style="flex:1;" onclick="event.stopPropagation(); window.showSuccessFromOwned('${p.id}')"><i class="fas fa-check"></i> Owned</button>`;
      } else if (isFree) {
        bBtn = `<button class="btn btn-free" style="flex:1;" onclick="event.stopPropagation(); initBuy('${p.id}')"><i class="fas fa-download"></i>Download</button>`;
      } else {
        bBtn = `<button class="btn" style="flex:1;" onclick="event.stopPropagation(); initBuy('${p.id}')"><i class="fas fa-shopping-cart"></i> Buy</button>`;
      }

      const priceDisplay = isFree ? `<span style="color:var(--success); font-size:18px;"><i class="fas fa-gift"></i> FREE</span>` : formatCurrency(p.price);

      return `
        <div class="product-card" onclick="openAbout('${p.id}')">
          <img src="${escapeHtml(p.thumbnail)}" class="product-image" onerror="this.src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='">
          <div class="product-title">${escapeHtml(p.title)}</div>
          <div class="product-price">${priceDisplay}</div>
          <div class="product-actions">
            <button class="btn btn-secondary" style="flex:1;" onclick="event.stopPropagation(); openAbout('${p.id}')"><i class="fas fa-info-circle"></i> Info</button>
            ${bBtn}
          </div>
        </div>
      `;
    }

    function renderProducts() {
      const paid = window.allProducts.filter(p => p.type === 'paid');
      const free = window.allProducts.filter(p => p.type === 'free');
      
      const pg = document.getElementById('paidGrid'); pg.innerHTML='';
      if(paid.length === 0) pg.innerHTML = '<div class="empty-state" style="grid-column: 1 / -1;"><i class="fas fa-box-open"></i><br><h3>No Premium Products Found</h3></div>';
      else paid.forEach(p => pg.innerHTML += getCardHTML(p));
      
      const fg = document.getElementById('freeGrid'); fg.innerHTML='';
      if(free.length === 0) fg.innerHTML = '<div class="empty-state" style="grid-column: 1 / -1;"><i class="fas fa-gift"></i><br><h3>No Free Products Found</h3></div>';
      else free.forEach(p => fg.innerHTML += getCardHTML(p));

      // Home Page rendering
      const hl = document.getElementById('homeLatestGrid'); hl.innerHTML='';
      const latestList = window.allProducts.slice(0,8);
      if(latestList.length === 0) hl.innerHTML = '<div class="empty-state" style="grid-column: 1 / -1;">No Products Available</div>';
      else latestList.forEach(p => hl.innerHTML += getCardHTML(p));
    }

    window.filterProducts = (type) => {
      const q = document.getElementById(type==='paid'?'searchPaid':'searchFree').value.toLowerCase();
      const grid = document.getElementById(type==='paid'?'paidGrid':'freeGrid');
      const arr = window.allProducts.filter(p => type === 'paid' ? p.type === 'paid' : p.type === 'free');
      
      grid.innerHTML='';
      const filtered = arr.filter(p => (p.title||'').toLowerCase().includes(q) || (p.category||'').toLowerCase().includes(q) || (p.tags||'').toLowerCase().includes(q));
      
      if(filtered.length === 0) {
          grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;"><i class="fas fa-search"></i><br><h3>No results found</h3></div>`;
      } else {
          filtered.forEach(p => grid.innerHTML += getCardHTML(p));
      }
    };

    window.showSuccessFromOwned = (id) => {
      const p = window.allProducts.find(x=>x.id===id);
      if(p) showSuccessModal(p.downloadLink);
    };

    // About Product
    window.openAbout = (id) => {
      const p = window.allProducts.find(x=>x.id===id); if(!p) return;
      document.getElementById('aboutImage').src = p.thumbnail;
      document.getElementById('aboutTitle').innerText = p.title;
      
      const isFree = p.type === 'free' || (!p.price || parseFloat(p.price)===0);
      const isOwned = hasPurchased(p.id);
      
      document.getElementById('aboutPrice').innerHTML = isFree ? '<span style="color:var(--success);"><i class="fas fa-gift"></i> FREE</span>' : formatCurrency(p.price);
      document.getElementById('aboutCategory').innerText = p.category || 'Software';
      document.getElementById('aboutVersion').innerText = p.version || '1.0';
      document.getElementById('aboutDesc').innerHTML = p.description || 'No description provided.';
      
      const gal = document.getElementById('aboutGallery'); gal.innerHTML='';
      if(p.images && p.images.length>0) { p.images.forEach(img => gal.innerHTML+=`<img src="${escapeHtml(img)}" onclick="window.open(this.src,'_blank')">`); }
      
      const act = document.getElementById('aboutActionBtn');
      if (isOwned) {
        act.innerHTML = `<button class="btn btn-free" style="width:100%; font-size:16px; padding:15px;" onclick="window.showSuccessFromOwned('${p.id}')"><i class="fas fa-check-circle"></i> View Download Link</button>`;
      } else if(isFree) {
        act.innerHTML = `<button class="btn btn-free" style="width:100%; font-size:16px; padding:15px;" onclick="initBuy('${p.id}')"><i class="fas fa-download"></i> Download Now</button>`;
      } else {
        act.innerHTML = `<button class="btn" style="width:100%; font-size:16px; padding:15px;" onclick="initBuy('${p.id}')"><i class="fas fa-bolt"></i> Purchase Product</button>`;
      }
      
      document.getElementById('aboutModal').classList.add('active');
    };

    // Buying / Downloading Logic
    window.initBuy = (id) => {
      if(!window.currentUser) { showAuthModal(); showNotification('Login required to continue','error'); return; }
      if(hasPurchased(id)) { window.showSuccessFromOwned(id); return; } // Duplicate Protection
      
      const p = window.allProducts.find(x=>x.id===id); if(!p) return;
      
      const isFree = p.type === 'free' || (!p.price || parseFloat(p.price) === 0);
      
      if(isFree) {
        processFreeDownload(p);
      } else {
        const amt = parseFloat(p.price || 0);
        processPaidPurchase(p, amt);
      }
    };

    async function processFreeDownload(p) {
      showLoading('GENERATING LINK...');
      try {
        // Record Order directly
        const oRef = window.dbPush(window.dbRef(window.db, 'orders'));
        const orderId = oRef.key;
        await window.dbSet(oRef, {
          productId: p.id, finalAmount: 0,
          productSnapshot: { title: p.title, imageUrl: p.thumbnail, discountedPrice: 0 },
          userInput: { name: window.currentUser.displayName||'User', email: window.currentUser.email, utrId: 'FREE_DOWNLOAD' },
          userId: window.currentUser.uid, status: 'confirmed', createdAt: new Date().toISOString()
        });

        // Update user stats for accurate download tracking safely for analytics Dashboard
        await window.dbSet(window.dbRef(window.db, `users/${window.currentUser.uid}/downloadedProducts/${p.id}`), {
          downloadedAt: new Date().toISOString()
        });
        
        hideLoading(); closeModal('aboutModal');
        showSuccessModal(p.downloadLink);
      } catch(e) { hideLoading(); showNotification(e.message,'error'); }
    }

    // Dynamic ZapUPI Implementation
    function processPaidPurchase(p, amt) {
      if(!window.pgSettings || !window.pgSettings.enabled) return showNotification('Payment gateway is currently disabled','error');
      if(!window.pgSettings.apiKey) return showNotification('Gateway configuration error from Admin','error');
      
      const orderId = "ORD" + Date.now() + window.currentUser.uid.substring(0,4);
      showLoading('INITIALIZING GATEWAY...');
      
      // Save Pending Order
      window.dbSet(window.dbRef(window.db, `pendingOrders/${orderId}`), {
        productId: p.id, title: p.title, image: p.thumbnail, dlLink: p.downloadLink,
        amount: amt, userId: window.currentUser.uid, status: 'pending', createdAt: new Date().toISOString()
      }).then(() => {
        // Send actual API Key fetched from Firebase
        ZapUPI.createOrder({ zap_key: window.pgSettings.apiKey, order_id: orderId, amount: amt.toString() }, {
          onResponse: function(url) { hideLoading(); ZapUPI.loadPayment(url); },
          onError: function(err) { hideLoading(); showNotification('Gateway Error: '+err,'error'); }
        });
      }).catch(err => { hideLoading(); showNotification('Failed: '+err.message,'error'); });
    }

    window.addEventListener('load', () => {
      if(typeof ZapUPI !== 'undefined') {
        ZapUPI.setPaymentCallbacks({
          onSuccess: function(oid) { verifyZapPayment(oid); },
          onFailed: function(oid) { hideLoading(); showNotification('Payment Failed','error'); },
          onTimeout: function(oid) { hideLoading(); showNotification('Payment Timeout','error'); }
        });
      }
    });

    async function verifyZapPayment(oid) {
      showLoading('VERIFYING PAYMENT...');
      // Use Dynamic API Key for Verification
      ZapUPI.orderStatus({ zap_key: window.pgSettings.apiKey, order_id: oid }, {
        onResponse: async function(a, d) {
          if(d.data.status === 'Success') {
            try {
              const poSnap = await window.dbGet(window.dbRef(window.db, `pendingOrders/${oid}`));
              if(!poSnap.exists()) throw new Error('Order verification failed or expired');
              const po = poSnap.val();

              const oRef = window.dbPush(window.dbRef(window.db, 'orders'));
              await window.dbSet(oRef, {
                productId: po.productId, finalAmount: po.amount,
                productSnapshot: { title: po.title, imageUrl: po.image, discountedPrice: po.amount },
                userInput: { name: window.currentUser.displayName||'User', email: window.currentUser.email, utrId: d.data.utr },
                userId: window.currentUser.uid, status: 'confirmed', createdAt: new Date().toISOString()
              });

              await window.dbPush(window.dbRef(window.db, 'payments'), {
                orderId: oid, uid: window.currentUser.uid, username: window.currentUser.displayName||'User',
                amount: po.amount, gateway: 'ZapUPI', status: 'Success', date: new Date().toISOString(), utr: d.data.utr
              });

              // Track in User purchases for Analytics Dashboard consistency
              await window.dbSet(window.dbRef(window.db, `users/${window.currentUser.uid}/purchasedProducts/${po.productId}`), {
                purchasedAt: new Date().toISOString(),
                amount: po.amount
              });

              await window.dbRemove(window.dbRef(window.db, `pendingOrders/${oid}`));
              
              hideLoading(); closeModal('aboutModal');
              showSuccessModal(po.dlLink);
            } catch(e) { hideLoading(); showNotification(e.message,'error'); }
          } else { hideLoading(); showNotification('Gateway rejected payment','error'); }
        },
        onError: function(e) { hideLoading(); showNotification('Verification Error: '+e,'error'); }
      });
    }

    // Success Modal
    function showSuccessModal(link) {
      document.getElementById('successLinkInput').value = link;
      document.getElementById('successOpenBtn').onclick = () => window.open(link, '_blank');
      document.getElementById('successModal').classList.add('active');
    }
    window.copySuccessLink = () => {
      const l = document.getElementById('successLinkInput'); l.select(); document.execCommand('copy');
      showNotification('Link Copied to Clipboard!');
    };

    // Orders & History Rendering
    window.renderOrders = () => {
      const q = document.getElementById('searchOrders').value.toLowerCase();
      const list = document.getElementById('ordersList'); list.innerHTML='';
      const arr = window.allOrders.filter(o => (o.productSnapshot?.title||'').toLowerCase().includes(q) || (o.id||'').toLowerCase().includes(q));
      
      if(arr.length===0) return list.innerHTML = `<div class="empty-state"><i class="fas fa-box-open"></i><br><h3>No Orders Found</h3></div>`;
      
      arr.forEach(o => {
        const p = window.allProducts.find(x=>x.id===o.productId);
        const dl = p ? p.downloadLink : '';
        const isPaid = parseFloat(o.finalAmount)>0;
        const oDate = new Date(o.createdAt).toLocaleDateString();
        
        list.innerHTML += `
          <div class="data-item">
            <img src="${escapeHtml(o.productSnapshot.imageUrl)}" class="data-img" onerror="this.src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='">
            <div style="flex:1;">
              <h3 style="color:var(--text-hi); font-size:16px;">${escapeHtml(o.productSnapshot.title)}</h3>
              <p style="font-family:var(--mono); font-size:12px; color:var(--text-mid);">ID: ${o.id.substring(0,8).toUpperCase()} | Date: ${oDate}</p>
              <p style="color:var(--signal); font-weight:bold;">${isPaid?formatCurrency(o.finalAmount):'<span style="color:var(--success);">FREE</span>'}</p>
            </div>
            <div style="display:flex; flex-direction:column; gap:5px; align-items:flex-end;">
              <span style="font-size:11px; padding:4px 8px; border-radius:6px; background:var(--signal-dim); color:var(--success); border:1px solid var(--success);">${o.status.toUpperCase()}</span>
              ${(o.status==='confirmed' && dl) ? `<button class="btn btn-free" style="padding:6px 12px; font-size:12px;" onclick="window.open('${escapeHtml(dl)}','_blank')"><i class="fas fa-download"></i> Download</button>` : ''}
            </div>
          </div>
        `;
      });
    };

    window.renderHistory = () => {
      const q = document.getElementById('searchHistory').value.toLowerCase();
      const list = document.getElementById('historyList'); list.innerHTML='';
      const arr = window.allPayments.filter(p => (p.orderId||'').toLowerCase().includes(q) || (p.utr||'').toLowerCase().includes(q));
      
      if(arr.length===0) return list.innerHTML = `<div class="empty-state"><i class="fas fa-file-invoice-dollar"></i><br><h3>No Transactions Found</h3></div>`;
      
      arr.forEach(p => {
        list.innerHTML += `
          <div class="data-item">
            <div style="width:40px; height:40px; border-radius:50%; background:var(--signal-dim); color:var(--signal); display:flex; align-items:center; justify-content:center; font-size:20px;"><i class="fas fa-receipt"></i></div>
            <div style="flex:1;">
              <h3 style="color:var(--text-hi); font-size:15px;">TXN: ${escapeHtml(p.utr||p.orderId)}</h3>
              <p style="font-family:var(--mono); font-size:12px; color:var(--text-mid);">Date: ${new Date(p.date).toLocaleString()} | Gateway: ${escapeHtml(p.gateway)}</p>
            </div>
            <div style="text-align:right;">
              <div style="color:var(--signal); font-weight:800; font-family:var(--mono); font-size:18px;">${formatCurrency(p.amount)}</div>
              <span style="font-size:11px; color:${p.status==='Success'?'var(--success)':'var(--red)'};">${p.status.toUpperCase()}</span>
            </div>
          </div>
        `;
      });
    };

  </script>
</body>
</html>

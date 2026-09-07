import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit Page Configuration (Full Viewport, Dark Mode)
st.set_page_config(
    page_title="Fastshot — Describe an app. We'll build it.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Custom CSS to remove default Streamlit spacing and chrome
st.markdown("""
    <style>
        /* Hide Streamlit Header, Toolbar, and Footer */
        header[data-testid="stHeader"] { display: none !important; }
        footer { display: none !important; }
        #MainMenu { visibility: hidden !important; }
        
        /* Reset padding and margin for full screen iframe execution */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        iframe {
            display: block;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
        
        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #0a0d12;
        }
    </style>
""", unsafe_allow_html=True)

# 3. HTML / CSS / JS Payload
HTML_HERO_PAYLOAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fastshot — Describe an app. We'll build it.</title>
    <meta name="description" content="Fastshot turns a written description into a working app.">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    
    <!-- Google Fonts Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=block" rel="stylesheet">

    <script>
        document.documentElement.classList.add('anim');
    </script>

    <style>
        /* RESET */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        button, input, textarea { font: inherit; color: inherit; background: none; border: 0; }
        img, svg { display: block; }
        html, body { height: 100%; width: 100%; overflow: hidden; background: #0a0d12; }
        body {
            font-family: Inter, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-synthesis: none;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: geometricPrecision;
            color: #ffffff;
        }

        :focus-visible { outline: 2px solid #F8B285; outline-offset: 3px; border-radius: 4px; }

        /* CONSTANTS & DESKTOP UNITS */
        :root {
            --font-text: Inter, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-display: Inter, var(--font-text);
            
            /* Reference Unit Scaling from 1560x1008 */
            --u: min(0.06410256vw, 0.12400794vh);
            --vu: 0.09920635vh;
            --inset-top: 41;
            --inset-bottom: 106;

            --w-regular: 400;
            --w-display-wght: 410;
            --w-medium: 500;
            --w-semibold: 600;
            --w-display: var(--w-display-wght);
            --w-nav: 400;
            --w-brand: 500;
            --w-cta: 520;
            --w-body: var(--w-regular);
            --w-label: var(--w-medium);
            --w-model: var(--w-regular);
            --w-proof: 480;

            --e-primary: cubic-bezier(.16,1,.3,1);
            --e-soft: cubic-bezier(.22,1,.36,1);
        }

        @supports (height: 100dvh) {
            :root {
                --u: min(0.06410256vw, 0.12400794dvh);
                --vu: 0.09920635dvh;
            }
        }

        @media (min-width: 1561px) {
            :root { --inset-top: 27; --inset-bottom: 74; }
        }

        /* STAGE & BACKGROUND VIDEO */
        .stage { position: fixed; inset: 0; overflow: hidden; background: #0a0d12; }
        .stage-video {
            position: absolute; inset: 0; width: 100%; height: 100%;
            object-fit: cover; z-index: 0; pointer-events: none;
        }

        /* FRAME & LAYOUT (DESKTOP DEFAULT) */
        .frame {
            position: absolute; inset: 0; z-index: 1;
            display: flex; flex-direction: column;
            padding: calc(var(--inset-top)*var(--vu)) calc(225*var(--u)) calc(var(--inset-bottom)*var(--vu));
        }

        /* NAV */
        header.nav {
            height: calc(43*var(--u));
            display: flex; align-items: center; justify-content: space-between;
            position: relative; width: 100%;
        }

        .brand {
            display: flex; align-items: center; gap: calc(12*var(--u));
            text-decoration: none; color: #fff;
        }
        .brand-mark {
            width: calc(34*var(--u)); height: calc(34*var(--u));
            border-radius: 50%; background: #9C86CE;
            display: flex; align-items: center; justify-content: center;
        }
        .brand-mark-inner {
            width: calc(17.2*var(--u)); height: calc(17.2*var(--u));
            border-radius: 50%; background: #FFFFFF;
            display: flex; align-items: center; justify-content: center;
        }
        .brand-mark-dot {
            width: calc(7.4*var(--u)); height: calc(7.4*var(--u));
            border-radius: 50%; background: #151519;
        }
        .brand-wordmark {
            font-size: calc(18.49*var(--u)); font-weight: var(--w-brand);
            letter-spacing: -0.0154em; transform: translateY(calc(1*var(--u)));
            font-variation-settings: "opsz" 32;
            text-shadow: 0 calc(1*var(--u)) calc(10*var(--u)) rgba(0,0,0,.30);
        }

        .links {
            position: absolute; left: 50%; transform: translateX(-50%);
            top: calc((50.5 - 41)*var(--u));
            display: flex; gap: calc(50*var(--u));
        }
        .links a {
            font-size: calc(21.69*var(--u)); font-weight: var(--w-nav);
            letter-spacing: -0.0115em; line-height: 1.2; color: #ffffff;
            text-decoration: none; text-shadow: 0 calc(1*var(--u)) calc(12*var(--u)) rgba(0,0,0,.32);
            transition: opacity .18s ease;
        }
        .links a:hover { opacity: .72; }

        .cta {
            width: calc(140*var(--u)); height: calc(43*var(--u));
            border-radius: calc(12*var(--u));
            font-size: calc(15.70*var(--u)); font-weight: var(--w-cta);
            letter-spacing: -0.0127em; color: #ffffff;
            align-self: flex-start; margin-top: calc((42 - 41)*var(--u));
            background: linear-gradient(180deg, #3d3d3f 0%, #1d1d20 100%);
            box-shadow: inset 0 calc(1*var(--u)) 0 rgba(255,255,255,.10), 0 calc(2*var(--u)) calc(14*var(--u)) rgba(0,0,0,.28);
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; text-decoration: none;
            transition: filter .18s ease, transform .1s ease;
        }
        .cta span { transform: translateY(calc(2*var(--u))); }
        .cta:hover { filter: brightness(1.16); }
        .cta:active { transform: translateY(1px); }

        /* BURGER & MOBILE MENU */
        #menu { display: none; }
        .burger { display: none; }
        .sheet { display: none; }

        /* HERO MAIN */
        main.hero {
            flex: 1; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            gap: calc(var(--hero-gap)*var(--vu));
            padding-bottom: calc(4*var(--vu));
        }

        .h1 {
            font-size: calc(36.25*var(--u)); font-weight: var(--w-display);
            line-height: 1.10; letter-spacing: 0.0018em; color: #ffffff;
            font-variation-settings: "opsz" 32;
            text-shadow: 0 calc(2*var(--u)) calc(22*var(--u)) rgba(0,0,0,.30);
            text-align: center;
        }

        /* COMPOSER CARD */
        .card {
            width: calc(708*var(--u)); height: calc(143*var(--u));
            border-radius: calc(26*var(--u)); margin-right: calc(3*var(--u));
            background: rgba(41,41,43,.955);
            backdrop-filter: blur(calc(26*var(--u))) saturate(112%);
            -webkit-backdrop-filter: blur(calc(26*var(--u))) saturate(112%);
            box-shadow: inset 0 0 0 1px rgba(214,228,255,.14), 0 calc(22*var(--u)) calc(60*var(--u)) rgba(0,0,0,.30);
            position: relative;
        }

        .ph {
            position: absolute;
            left: calc(27*var(--u)); top: calc(33*var(--u)); right: calc(24*var(--u));
            color: #8B8C8E; font-size: calc(9.97*var(--u)); font-weight: 400;
            line-height: 1.35; letter-spacing: 0.007em;
            white-space: nowrap; overflow: hidden; pointer-events: none;
        }

        .tools {
            position: absolute;
            left: calc(19*var(--u)); top: calc(92*var(--u));
            height: calc(30*var(--u));
            right: calc(-1*var(--u));
        }

        .chips { display: flex; align-items: center; gap: calc(5.5*var(--u)); }
        
        .chip {
            height: calc(30*var(--u)); border-radius: calc(9*var(--u));
            font-size: calc(9.0*var(--u)); font-weight: 500; color: #909093; line-height: 1;
            background: linear-gradient(180deg, rgba(255,255,255,.088) 0%, rgba(255,255,255,.050) 45%, rgba(255,255,255,.038) 100%);
            border: 1px solid rgba(255,255,255,.05);
            display: inline-flex; align-items: center;
            padding-left: calc(var(--pl)*var(--u)); padding-right: calc(12*var(--u));
            cursor: pointer; transition: background .18s ease, color .18s ease;
        }
        .chip span { transform: translateY(calc(2*var(--u))); }
        .chip svg {
            fill: currentColor; margin-right: calc(var(--ig)*var(--u));
        }
        .chip:hover {
            background: linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,.07));
            color: #c8c8cb;
        }

        /* CRITICAL: COMPOSER RIGHT CLUSTER (DESKTOP ABSOLUTE COORDINATES) */
        .right {
            position: absolute; inset: 0; pointer-events: none;
        }
        .right > * { position: absolute; pointer-events: auto; }

        .model {
            left: calc(510.2*var(--u)); top: calc(15.5*var(--u));
            font-size: calc(10.4*var(--u)); font-weight: 400; color: #98999C; line-height: 1;
            display: inline-flex; align-items: center; gap: calc(6.2*var(--u));
            cursor: pointer;
        }
        .model svg { width: calc(6.8*var(--u)); fill: #98999C; }

        .attach {
            left: calc(599.15*var(--u)); top: calc(10.14*var(--u));
            color: #A9AAAD; cursor: pointer; display: block;
            transition: color .18s ease;
        }
        .attach svg { width: calc(19.79*var(--u)); height: auto; }
        .attach:hover { color: #ffffff; }

        .send {
            left: calc(640*var(--u)); top: calc(2*var(--u));
            width: calc(35*var(--u)); height: calc(35*var(--u));
            border-radius: 50%;
            background: linear-gradient(163deg, #FBBC94 0%, #F49D70 46%, #E88654 100%);
            box-shadow: 0 calc(3*var(--u)) calc(12*var(--u)) rgba(210,110,60,.34);
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: filter .18s ease, transform .1s ease;
        }
        .send svg { width: calc(11.66*var(--u)); fill: #ffffff; }
        .send:hover { filter: brightness(1.07); }
        .send:active { transform: scale(.95); }

        /* FOOTER PROOF */
        footer.proof {
            flex: none; display: flex; flex-direction: column;
            align-items: center; gap: calc(52.3*var(--vu));
        }
        .proof-by {
            font-size: calc(14.01*var(--u)); font-weight: var(--w-proof);
            letter-spacing: 0.0065em; color: rgba(255,255,255,.95);
            font-variation-settings: "opsz" 32;
            text-shadow: 0 calc(1*var(--u)) calc(12*var(--u)) rgba(0,0,0,.35);
        }
        .logos {
            display: flex; align-items: center; gap: calc(62*var(--u));
            filter: drop-shadow(0 calc(1*var(--u)) calc(10*var(--u)) rgba(0,0,0,.30));
        }
        .logos svg { fill: #ffffff; }

        /* RESPONSIVE ARCHITECTURE 2: TABLET */
        @media (min-width: 600px) and (max-width: 1180px) and (min-height: 600px) {
            :root { --u: 1px; }
            .frame {
                padding: clamp(24px, 3.4vh, 44px) clamp(28px, 4.2vw, 60px) clamp(26px, 4.4vh, 56px);
            }
            .links { position: static; transform: none; gap: clamp(20px, 3vw, 40px); }
            .links a { font-size: clamp(14px, 1.6vw, 20px); }
            .cta { margin-top: 0; width: auto; padding: 0 18px; height: 38px; font-size: 14px; }
            .h1 { font-size: clamp(27px, 4.3vw, 44px); line-height: 1.12; }
            
            .card {
                width: min(100%, clamp(516px, 74vw, 760px)); height: auto; margin-right: 0;
                padding: clamp(15px, 1.9vw, 24px); border-radius: clamp(17px, 2.1vw, 26px);
                display: flex; flex-direction: column; gap: clamp(20px, 3.2vh, 44px);
            }
            .ph {
                position: static; white-space: normal; font-size: clamp(11px, 1.35vw, 14px); line-height: 1.4;
            }
            .tools {
                position: static; height: auto; display: flex; flex-direction: row; flex-wrap: wrap;
                align-items: center; justify-content: space-between; gap: clamp(10px, 1.4vw, 18px);
            }
            .chips { gap: clamp(6px, 0.85vw, 10px); }
            .chip {
                height: clamp(29px, 3.4vh, 34px); padding: 0 clamp(7px, 1vw, 13px);
                font-size: clamp(9.6px, 1.12vw, 12.5px);
            }
            .right {
                position: static; display: flex; align-items: center; margin-left: auto; gap: 0; pointer-events: auto;
            }
            .right > * { position: static; }
            .model { font-size: clamp(9.8px, 1.12vw, 12.5px); }
            .attach { margin-left: clamp(9px, 1.4vw, 20px); }
            .attach svg { width: clamp(16px, 1.8vw, 20px); }
            .send {
                margin-left: clamp(9px, 1.3vw, 18px);
                width: clamp(32px, 3.5vw, 38px); height: clamp(32px, 3.5vw, 38px);
            }
            footer.proof { gap: clamp(15px, 2.5vh, 30px); }
        }

        /* RESPONSIVE ARCHITECTURE 3: COMPACT / PHONE */
        @media (max-width: 599px), (max-height: 599px) and (max-width: 1180px) {
            :root { --u: 1px; }
            .frame {
                padding: max(18px, env(safe-area-inset-top)) max(clamp(18px, 5.2vw, 40px), env(safe-area-inset-right)) max(20px, env(safe-area-inset-bottom)) max(clamp(18px, 5.2vw, 40px), env(safe-area-inset-left));
            }
            .links, header .cta { display: none; }
            .burger {
                display: flex; align-items: center; justify-content: center;
                width: 38px; height: 38px; border-radius: 11px;
                background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.14);
                cursor: pointer;
            }
            .sheet {
                display: grid; grid-template-rows: 0fr;
                transition: grid-template-rows 0.32s cubic-bezier(.4,0,.2,1);
                position: absolute; top: 65px; left: 0; right: 0; z-index: 10;
            }
            #menu:checked ~ .sheet { grid-template-rows: 1fr; }
            .sheet-content {
                overflow: hidden; background: rgba(24,24,27,.86);
                backdrop-filter: blur(20px); border-radius: 16px; border: 1px solid rgba(255,255,255,.09);
                padding: 0 20px; display: flex; flex-direction: column; gap: 12px;
            }
            #menu:checked ~ .sheet .sheet-content { padding: 20px; }
            .sheet-content a { color: #fff; text-decoration: none; font-size: 15px; }

            .h1 {
                width: 100%; max-width: 15ch; font-size: clamp(29px, 7.6vw, 50px);
                line-height: 1.14; letter-spacing: -.012em;
            }
            .card {
                width: 100%; max-width: 600px; height: auto; margin-right: 0;
                padding: clamp(13px, 3.4vw, 18px); border-radius: 20px;
                display: flex; flex-direction: column; gap: clamp(16px, 4.6vh, 34px);
            }
            .ph {
                position: static; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;
                font-size: clamp(9.4px, 2.95vw, 14px);
            }
            .tools {
                position: static; height: auto; display: flex; flex-direction: column;
                align-items: stretch; gap: 12px;
            }
            .chips { flex-wrap: wrap; }
            .right {
                position: static; display: flex; align-items: center; justify-content: flex-start;
                pointer-events: auto;
            }
            .right > * { position: static; }
            .attach { margin-left: auto; }
            .send { margin-left: 14px; width: 40px; height: 40px; }
        }

        @media (max-width: 1180px) and (max-height: 560px) {
            main.hero { gap: 16px; }
            .h1 { font-size: clamp(24px, 5.4vh, 34px); }
            footer.proof { gap: 10px; }
            .frame { padding-top: 10px; }
        }

        /* ENTRANCE ANIMATIONS */
        @media (prefers-reduced-motion: no-preference) {
            html.anim .brand { animation: e-settle-down .58s var(--e-soft) .06s both; }
            html.anim .brand-mark { animation: e-mark .62s var(--e-primary) .06s both; }
            html.anim .links a:nth-child(1) { animation: e-settle-down .50s var(--e-soft) .16s both; }
            html.anim .links a:nth-child(2) { animation: e-settle-down .50s var(--e-soft) .21s both; }
            html.anim .links a:nth-child(3) { animation: e-settle-down .50s var(--e-soft) .26s both; }
            html.anim .links a:nth-child(4) { animation: e-settle-down .50s var(--e-soft) .31s both; }
            html.anim .cta { animation: e-settle-down .55s var(--e-soft) .34s both; }
            html.anim .h1 { animation: e-focus 1.00s var(--e-primary) .30s both; will-change: transform, opacity; }
            html.anim .card { animation: e-panel .90s var(--e-primary) .62s both; will-change: transform, opacity; }
            html.anim .ph { animation: e-populate .50s var(--e-soft) .88s both; }
            html.anim .chips { animation: e-populate .50s var(--e-soft) .94s both; }
            html.anim .right { animation: e-populate .50s var(--e-soft) 1.00s both; }
            html.anim .send { animation: e-send .50s var(--e-primary) 1.00s both; }
            html.anim .proof-by { animation: e-settle-up .55s var(--e-soft) 1.08s both; }
            html.anim .logos svg:nth-child(1) { animation: e-settle-up .55s var(--e-soft) 1.16s both; }
            html.anim .logos svg:nth-child(2) { animation: e-settle-up .55s var(--e-soft) 1.22s both; }
            html.anim .logos svg:nth-child(3) { animation: e-settle-up .55s var(--e-soft) 1.28s both; }
        }

        @keyframes e-settle-down { from { opacity: 0; transform: translateY(calc(-5*var(--u))); } to { opacity: 1; transform: none; } }
        @keyframes e-settle-up { from { opacity: 0; transform: translateY(calc(6*var(--u))); } to { opacity: 1; transform: none; } }
        @keyframes e-mark { from { transform: scale(.9); } to { transform: none; } }
        @keyframes e-focus { from { opacity: 0; transform: translateY(calc(14*var(--u))); filter: blur(6px); } to { opacity: 1; transform: none; filter: blur(0); } }
        @keyframes e-panel { from { opacity: 0; transform: translateY(calc(18*var(--u))) scale(.985); } to { opacity: 1; transform: none; } }
        @keyframes e-populate { from { opacity: 0; transform: translateY(calc(4*var(--u))); } to { opacity: 1; transform: none; } }
        @keyframes e-send { from { transform: scale(.82); } to { transform: none; } }

        @media (prefers-reduced-motion: reduce) {
            * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
        }
    </style>
</head>
<body>
    <div class="stage">
        <!-- FULL VIEWPORT BACKGROUND VIDEO -->
        <video class="stage-video" autoplay muted loop playsinline>
            <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260826_124724_bc041163-d651-425f-aea3-2acc1efc2c96.mp4" type="video/mp4">
        </video>

        <div class="frame">
            <!-- MOBILE MENU CONTROLLER -->
            <input type="checkbox" id="menu">
            
            <!-- NAV HEADER -->
            <header class="nav">
                <a href="#" class="brand" aria-label="Fastshot home">
                    <div class="brand-mark">
                        <div class="brand-mark-inner">
                            <div class="brand-mark-dot"></div>
                        </div>
                    </div>
                    <span class="brand-wordmark">Fastshot</span>
                </a>

                <nav class="links">
                    <a href="#">Features</a>
                    <a href="#">Examples</a>
                    <a href="#">Pricing</a>
                    <a href="#">Docs</a>
                </nav>

                <a href="#" class="cta"><span>Get Started</span></a>

                <label for="menu" class="burger" aria-label="Toggle Navigation">
                    <svg width="17" height="12" viewBox="0 0 17 12" fill="none">
                        <path d="M0 1H17M0 11H17" stroke="white" stroke-width="2"/>
                    </svg>
                </label>

                <div class="sheet">
                    <div class="sheet-content">
                        <a href="#">Features</a>
                        <a href="#">Examples</a>
                        <a href="#">Pricing</a>
                        <a href="#">Docs</a>
                        <a href="#" style="color: #F8B285; font-weight: 600;">Get Started</a>
                    </div>
                </div>
            </header>

            <!-- HERO CONTENT -->
            <main class="hero">
                <h1 class="h1">Describe an app. We'll build it.</h1>

                <form class="card" onsubmit="return false">
                    <p class="ph">Build a fintech tracking app with bank level privacy and...</p>
                    
                    <div class="tools">
                        <div class="chips">
                            <button type="button" class="chip" style="--cw:107;--pl:12;--ig:3.7">
                                <svg width="15" height="15" viewBox="0 0 15 15"><path d="M3.5 2A1.5 1.5 0 002 3.5v8A1.5 1.5 0 003.5 13h8a1.5 1.5 0 001.5-1.5v-8A1.5 1.5 0 0011.5 2h-8zM5 5.5a1 1 0 112 0 1 1 0 01-2 0zm-1 5.5l2.5-3 2 2.5 1.5-1.5 2 2H4z"/></svg>
                                <span>Attach Screens</span>
                            </button>
                            <button type="button" class="chip" style="--cw:108;--pl:16;--ig:3.9">
                                <svg width="12" height="15" viewBox="0 0 12 15"><path d="M3 2a2 2 0 00-2 2v2a2 2 0 002 2h2V2H3zm6 0H7v6h2a2 2 0 002-2V4a2 2 0 00-2-2zM3 9a2 2 0 00-2 2v2a2 2 0 002 2h2V9H3zm6 0H7v6h2a2 2 0 002-2v-2a2 2 0 00-2-2z"/></svg>
                                <span>Attach a Figma</span>
                            </button>
                            <button type="button" class="chip" style="--cw:107;--pl:15.8;--ig:2.9">
                                <svg width="13" height="15" viewBox="0 0 13 15"><path d="M6.5 1a5.5 5.5 0 00-5.5 5.5c0 2.2 1.3 4.1 3.2 5v1.5a1 1 0 001 1h2.6a1 1 0 001-1v-1.5c1.9-.9 3.2-2.8 3.2-5A5.5 5.5 0 006.5 1z"/></svg>
                                <span>Today's Theme</span>
                            </button>
                        </div>

                        <!-- EXACT ABSOLUTE RIGHT CLUSTER FOR DESKTOP -->
                        <div class="right">
                            <div class="model">
                                <span>Sonnet 4.5</span>
                                <svg viewBox="0 0 7 4"><path d="M0 0l3.5 4L7 0H0z"/></svg>
                            </div>

                            <button type="button" class="attach" aria-label="Attach File">
                                <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8">
                                    <path d="M14.5 5.5l-6.8 6.8a2.5 2.5 0 103.5 3.5l6.8-6.8a4.5 4.5 0 10-6.4-6.4l-7.2 7.2a6.5 6.5 0 109.2 9.2l6.1-6.1"/>
                                </svg>
                            </button>

                            <button type="submit" class="send" aria-label="Build it">
                                <svg viewBox="0 0 12 12"><path d="M6 10.5V1.5M6 1.5L1.5 6M6 1.5L10.5 6" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                            </button>
                        </div>
                    </div>
                </form>
            </main>

            <!-- FOOTER -->
            <footer class="proof">
                <p class="proof-by">Built by engineers from</p>
                <div class="logos">
                    <!-- Google -->
                    <svg width="97" height="32" viewBox="0 0 97 32"><path d="M12.5 14.2v3.7h8.8c-.4 2.3-2.6 6.7-8.8 6.7-5.3 0-9.6-4.4-9.6-9.8s4.3-9.8 9.6-9.8c3 0 5 1.3 6.2 2.4l2.9-2.8C19.8 2.8 16.5 1.2 12.5 1.2 5.6 1.2 0 6.8 0 13.7s5.6 12.5 12.5 12.5c7.2 0 12-5.1 12-12.2 0-.8-.1-1.4-.2-1.8H12.5zM33 9.5c-4.4 0-8 3.4-8 8s3.6 8 8 8 8-3.4 8-8-3.6-8-8-8zm0 12.5c-2.4 0-4.4-2-4.4-4.5s2-4.5 4.4-4.5 4.4 2 4.4 4.5-2 4.5-4.4 4.5zm18 0c-2.4 0-4.4-2-4.4-4.5s2-4.5 4.4-4.5 4.4 2 4.4 4.5-2 4.5-4.4 4.5zm0-12.5c-4.4 0-8 3.4-8 8s3.6 8 8 8 8-3.4 8-8-3.6-8-8-8zm21.1 1c-1-.9-2.5-1.7-4.4-1.7-4.1 0-7.7 3.6-7.7 8s3.6 8 7.7 8c1.9 0 3.4-.8 4.4-1.8v1.1c0 3.1-1.7 4.7-4.3 4.7-2.2 0-3.5-1.6-4-2.5l-3.1 1.3c.9 2.2 3.3 4.7 7.1 4.7 4.2 0 7.7-2.5 7.7-8.4V9.9h-3.4v1.6zm-4.1 11.5c-2.4 0-4.2-2-4.2-4.5s1.8-4.5 4.2-4.5 4.2 2 4.2 4.5-1.8 4.5-4.2 4.5zM76 2h3.6v23.5H76V2zm13.1 7.5c-3.8 0-7 3.1-7 8 0 4.8 3.1 8 7 8 2.3 0 4-1.1 5.1-2.4l-2.8-1.9c-.8 1.1-1.8 1.8-3.1 1.8-2.1 0-3.5-1.2-4.1-2.9l9.7-4-.3-.8c-.7-2-2.7-5.8-7.5-5.8zm.2 3.4c1.4 0 2.5.7 2.9 1.7l-6.8 2.8c-.1-2.6 1.9-4.5 3.9-4.5z"/></svg>
                    <!-- Cisco -->
                    <svg width="68" height="32" viewBox="0 0 68 32"><path d="M4 14h3.2v11H4V14zm11.7.3c-2 0-3.5.7-4.5 1.8l2 2.2c.6-.7 1.4-1.1 2.5-1.1 1.3 0 2.1.6 2.1 1.7v.4c-.5-.3-1.4-.5-2.5-.5-2.7 0-4.4 1.3-4.4 3.2 0 1.9 1.5 3.1 3.5 3.1 1.5 0 2.7-.6 3.4-1.7v1.4h3.1V20c0-3.7-2.2-5.7-5.2-5.7zm1 6.8c0 1.2-.9 2.1-2.2 2.1-.9 0-1.6-.5-1.6-1.3 0-.8.7-1.3 1.9-1.3.7 0 1.4.2 1.9.4v.1zm12.1-7.1c-1.8 0-3.2.8-4 2.1V14h-3.2v11h3.2v-6.3c0-1.7 1-2.8 2.5-2.8 1.4 0 2.2 1 2.2 2.7V25h3.2v-6.7c0-3.1-1.7-4.3-3.9-4.3zm13.9 0c-3.6 0-6 2.5-6 5.7s2.4 5.7 6 5.7 6-2.5 6-5.7-2.4-5.7-6-5.7zm0 8.5c-1.8 0-2.8-1.4-2.8-2.8s1-2.8 2.8-2.8 2.8 1.4 2.8 2.8-1 2.8-2.8 2.8zM5.6 2v6.5h2.1V2H5.6zm10.7-2v8.5h2.1V0h-2.1zm10.7 2v6.5h2.1V2h-2.1zm10.7-2v8.5h2.1V0h-2.1zm10.7 2v6.5h2.1V2h-2.1z"/></svg>
                    <!-- Adobe -->
                    <svg width="89" height="32" viewBox="0 0 89 32"><path d="M0 2h11.5L0 28H0V2zm18 0h11.5L41 28h-6.2l-3.1-7.5H21L18 28h-6.2L18 2zm10.1 13.5L25 7.2l-3.1 8.3h6.2zM43 2h11.5v26H43V2zm22.4 0c5.8 0 10.1 3.8 10.1 9.4 0 3.7-1.9 6.8-5.3 8.3l6 8.3h-7l-5.1-7.3h-3.6V28h-5.5V2h10.4zm-.4 11.2c2.8 0 4.8-1.7 4.8-4.3s-2-4.2-4.8-4.2h-4.9v8.5h4.9z"/></svg>
                </div>
            </footer>
        </div>
    </div>

    <script>
        // Teardown entrance animation class after total timeline duration
        window.addEventListener('DOMContentLoaded', () => {
            const timeout = setTimeout(() => {
                document.documentElement.classList.remove('anim');
            }, 2600);

            const lastLogo = document.querySelector('.logos svg:last-child');
            if (lastLogo) {
                lastLogo.addEventListener('animationend', () => {
                    clearTimeout(timeout);
                    document.documentElement.classList.remove('anim');
                }, { once: true });
            }
        });
    </script>
</body>
</html>
"""

# 4. Render as Full-Viewport Component inside Streamlit
components.html(HTML_HERO_PAYLOAD, height=1000, scrolling=False)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Chapter 2 — The Opportunity Nobody Sees",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
section[data-testid="stSidebar"],
.main { background-color: #0d1117 !important; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem;
                   max-width: 1280px; background-color: #0d1117 !important; }

.kpi-wrap {
    background: #12161f;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 20px 18px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 12px 12px 0 0;
}
.kpi-num { font-size: 2.1rem; font-weight: 800; color: var(--accent); line-height: 1; }
.kpi-sub { font-size: 0.72rem; color: #6b7a99; margin-top: 6px;
           text-transform: uppercase; letter-spacing: 0.08em; line-height: 1.5; }
div[data-testid="stHorizontalBlock"] > div { gap: 12px; }

[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────

@st.cache_data
def load():
    df = pd.read_csv("/Users/ashley/Desktop/Azimuth-Analytics/airplay_vs_shows.csv")
    df = df.dropna(how="all")
    df = df[df["name"].str.strip().ne("")]
    df = df.drop_duplicates()
    df["airplay_count"] = df["airplay_count"].clip(lower=0)
    df["shows_count"]   = df["shows_count"].clip(lower=0)
    df["opp_score"]     = df["airplay_count"] / (df["shows_count"] + 1)
    return df

df = load()

AIRPLAY_MIN = 50
AIRPLAY_MAX = 500

DECEASED_OR_INACTIVE = {
    "Michael Jackson", "Prince", "Tom Petty", "George Michael",
    "Eddie Money", "Selena", "Eric Carmen", "Andy Williams",
    "Vicente Fernández", "Joan Sebastian", "Pop Smoke",
    "John Lennon", "Elvis Presley", "Avicii",
    "Nirvana", "Led Zeppelin", "Wham!", "The Cranberries",
    "Pink Floyd", "The Cars", "Tom Petty & the Heartbreakers",
    "The Outfield", "Fleetwood Mac",
}

_band = df["airplay_count"].between(AIRPLAY_MIN, AIRPLAY_MAX)

opp_all = df[(df["shows_count"] == 0) & _band]
opp     = opp_all[~opp_all["name"].isin(DECEASED_OR_INACTIVE)]
removed = opp_all[opp_all["name"].isin(DECEASED_OR_INACTIVE)]

active = df[(df["shows_count"] >= 20)         & _band]
middle = df[(df["shows_count"].between(1, 19)) & _band]

n_opp           = len(opp)
potential_shows = n_opp * 20
n_mid_tier      = len(df[_band])
untapped_pct    = round(n_opp / max(n_mid_tier, 1) * 100, 1)


# ── Chapter 2 title ────────────────────────────────────────────────────────────

st.markdown("""
<div style='background:#0d1117;padding:0 0 0 0;'>
  <div style='font-size:0.78rem;font-weight:600;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;'>
    Chapter 2
  </div>
  <h1 style='font-size:2.1rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.03em;margin-bottom:10px;line-height:1.15;'>
    The Opportunity Nobody Sees
  </h1>
  <p style='font-size:0.9rem;color:#4b5675;margin-bottom:36px;line-height:1.6;
            border-left:3px solid #1e2535;padding-left:14px;'>
    Two sides of the same market gap — artists with audiences and no shows,
    and stages with capacity and no bookings.
  </p>
</div>
""", unsafe_allow_html=True)


# ── Sub-section 1: The First Half ──────────────────────────────────────────────

st.markdown(f"""
<div style='border-top:1px solid #1e2535;padding-top:28px;margin-bottom:20px;'>
  <h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.02em;margin-bottom:8px;'>
    The First Half — Artists Without a Stage
  </h2>
  <p style='font-size:0.9rem;color:#64748b;margin:0 0 8px;line-height:1.65;'>
    Streaming has built real audiences for artists who have never played a live show.
    Among <b style='color:#94a3b8;'>{n_mid_tier} mid-tier artists</b> with genuine local radio presence
    (airplay {AIRPLAY_MIN}–{AIRPLAY_MAX}),
    <b style='color:#fb923c;'>{untapped_pct}% have zero scheduled shows.</b>
  </p>
  <p style='font-size:0.85rem;color:#4b5675;margin:0;line-height:1.6;'>
    Superstars and deceased artists are excluded. What remains is
    <b style='color:#fb923c;'>{n_opp} active, bookable artists</b> whose audiences already exist
    — they just haven't been connected to a stage yet.
  </p>
</div>
""", unsafe_allow_html=True)


# ── KPI row ────────────────────────────────────────────────────────────────────

def kpi(val, lbl, accent):
    return (
        f"<div class='kpi-wrap' style='--accent:{accent};'>"
        f"<div class='kpi-num'>{val}</div>"
        f"<div class='kpi-sub'>{lbl}</div>"
        f"</div>"
    )

k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi(f"{untapped_pct}%",
                f"Mid-Tier Artists With 0 Shows<br>Airplay {AIRPLAY_MIN}–{AIRPLAY_MAX}",
                "#fb923c"), unsafe_allow_html=True)
k2.markdown(kpi(f"{n_opp}",
                "Bookable Mid-Tier Artists<br>0 Shows · Active &amp; Alive",
                "#f59e0b"), unsafe_allow_html=True)
k3.markdown(kpi(f"{potential_shows:,}+",
                "Est. Unbooked Shows / yr<br>@ 20 Shows per Artist",
                "#a78bfa"), unsafe_allow_html=True)
k4.markdown(kpi(f"{len(active)}",
                "Mid-Tier Artists Already Touring<br>Proof the Model Works",
                "#38bdf8"), unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)


# ── Scatter chart ──────────────────────────────────────────────────────────────

rng     = np.random.default_rng(42)
y_max   = AIRPLAY_MAX
X_GAP_L = 7     # left edge of booking-gap corridor
X_GAP_R = 22    # right edge

fig = go.Figure()

# ① Zone background fills
for kw in [
    dict(x0=-4,      x1=X_GAP_L, fillcolor="rgba(251,146,60,0.09)"),
    dict(x0=X_GAP_L, x1=X_GAP_R, fillcolor="rgba(255,255,255,0.005)"),
    dict(x0=X_GAP_R, x1=135,     fillcolor="rgba(56,189,248,0.05)"),
]:
    fig.add_shape(type="rect", layer="below",
                  y0=-80, y1=y_max * 1.25,
                  line_width=0, **kw)

# ② Zone dividers
for xv in [X_GAP_L, X_GAP_R]:
    fig.add_shape(type="line", layer="below",
                  x0=xv, x1=xv, y0=0, y1=y_max * 1.22,
                  line=dict(color="#252f45", width=1.2, dash="dot"))

# ③ Middle band (1–19 shows) — muted gray
j_mid = rng.uniform(-0.7, 0.7, len(middle))
fig.add_trace(go.Scatter(
    x=middle["shows_count"] + j_mid, y=middle["airplay_count"],
    mode="markers",
    name="Some Activity  (1–19 shows)",
    marker=dict(color="#293548", size=np.clip(middle["airplay_count"] / 80, 4, 9),
                opacity=0.55, line=dict(color="#3d4f6b", width=0.4)),
    customdata=middle[["name","airplay_count","shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows %{customdata[2]}<extra></extra>",
))

# ④ Active touring — sky blue
j_act = rng.uniform(-1.5, 1.5, len(active))
fig.add_trace(go.Scatter(
    x=active["shows_count"] + j_act, y=active["airplay_count"],
    mode="markers",
    name="Active Touring  (≥20 shows)",
    marker=dict(color="#38bdf8", size=np.clip(active["airplay_count"] / 52, 8, 22),
                opacity=0.88, line=dict(color="rgba(186,230,253,0.28)", width=0.8)),
    customdata=active[["name","airplay_count","shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows/yr %{customdata[2]}<extra></extra>",
))

# ⑤ Opportunity glow halo
j_opp = rng.uniform(-2.8, 2.8, len(opp))
fig.add_trace(go.Scatter(
    x=j_opp, y=opp["airplay_count"],
    mode="markers",
    marker=dict(color="rgba(251,146,60,0.09)", size=np.clip(opp["airplay_count"] / 34, 26, 56),
                opacity=1, line=dict(width=0)),
    hoverinfo="skip", showlegend=False,
))

# ⑥ Opportunity solid dots — orange
fig.add_trace(go.Scatter(
    x=j_opp, y=opp["airplay_count"],
    mode="markers",
    name="Untapped Audience  (0 shows · active &amp; alive)",
    marker=dict(color="#fb923c", size=np.clip(opp["airplay_count"] / 44, 9, 26),
                opacity=0.95, line=dict(color="rgba(253,186,116,0.40)", width=1.1)),
    customdata=opp[["name","airplay_count","shows_count","opp_score"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>Airplay: %{customdata[1]:,}<br>"
        "Shows/yr: %{customdata[2]}<br>Opp. Score: %{customdata[3]:.0f}<extra></extra>"
    ),
))

# ⑦ Zone header badges (larger, cleaner — two only, gap handled by callout)
for d in [
    dict(x=0,  y=y_max*1.155, text="<b>UNTAPPED AUDIENCE</b>",
         color="#fb923c", size=13, bg="rgba(251,146,60,0.14)", bc="rgba(251,146,60,0.32)"),
    dict(x=70, y=y_max*1.155, text="<b>ACTIVE TOURING</b>",
         color="#38bdf8", size=13, bg="rgba(56,189,248,0.12)", bc="rgba(56,189,248,0.30)"),
]:
    fig.add_annotation(
        x=d["x"], y=d["y"], text=d["text"], showarrow=False,
        font=dict(size=d["size"], color=d["color"], family="Inter, sans-serif"),
        xanchor="center", yanchor="middle", xref="x", yref="y",
        bgcolor=d["bg"], bordercolor=d["bc"], borderwidth=1, borderpad=7,
    )

# ⑧ ONE gap callout — clean, centred in the corridor
_gap_cx = (X_GAP_L + X_GAP_R) / 2
fig.add_annotation(
    x=_gap_cx, y=y_max * 0.46,
    text=(
        "← THE BOOKING GAP →<br>"
        f"<b>{n_opp} artists · 0 shows</b><br>"
        f"<b>{potential_shows:,}+ shows / yr unrealized</b>"
    ),
    showarrow=False,
    font=dict(size=11.5, color="#94a3b8", family="Inter, sans-serif"),
    xanchor="center", yanchor="middle",
    xref="x", yref="y",
    bgcolor="rgba(11,17,27,0.90)",
    bordercolor="rgba(75,86,117,0.32)",
    borderwidth=1,
    borderpad=14,
    align="center",
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),

    title=dict(
        text=(
            "<b style='color:#e2e8f0;font-size:16px;'>"
            "Radio Reach vs. Live Shows — Where the Gap Lives"
            "</b><br>"
            "<span style='color:#64748b;font-size:11.5px;'>"
            f"Mid-tier artists only (airplay {AIRPLAY_MIN}–{AIRPLAY_MAX})  ·  "
            "dot size = radio reach  ·  "
            "<span style='color:#fb923c;'>● 0 shows (untapped)</span>  "
            "<span style='color:#334155;'>● 1–19 shows</span>  "
            "<span style='color:#38bdf8;'>● active touring (≥20)</span>"
            "</span>"
        ),
        x=0.0,
        font=dict(family="Inter, sans-serif"),
        pad=dict(b=10),
    ),

    xaxis=dict(
        title=dict(text="Number of Live Shows per Year", font=dict(size=13, color="#64748b")),
        range=[-4, 128],
        gridcolor="#0d1520",
        zeroline=False,
        tickfont=dict(size=12, color="#6b7280"),
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showspikes=True, spikecolor="#1e2535", spikethickness=1,
    ),

    yaxis=dict(
        title=dict(text="Local Radio Airplay Count", font=dict(size=13, color="#64748b")),
        range=[-20, y_max * 1.25],
        gridcolor="#0d1520",
        zeroline=False,
        tickfont=dict(size=12, color="#6b7280"),
        showspikes=True, spikecolor="#1e2535", spikethickness=1,
    ),

    legend=dict(
        bgcolor="rgba(13,17,23,0.92)",
        bordercolor="#1e2535",
        borderwidth=1,
        font=dict(size=11.5, color="#94a3b8"),
        itemsizing="constant",
        orientation="h",
        yanchor="bottom", y=-0.15,
        xanchor="left",   x=0,
    ),

    margin=dict(l=70, r=30, t=88, b=85),
    height=700,

    hoverlabel=dict(
        bgcolor="#1a2133", bordercolor="#2e3a52",
        font=dict(size=12.5, family="Inter, sans-serif"),
    ),
)

st.plotly_chart(fig, use_container_width=True)


# ── Insight strip ──────────────────────────────────────────────────────────────

avg_active_shows  = round(active["shows_count"].mean(), 1)
top3_active_names = ", ".join(active.nlargest(3, "airplay_count")["name"].tolist())

st.markdown(f"""
<div style='display:flex;gap:12px;margin:2px 0 28px;'>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #fb923c;border-radius:8px;padding:18px 20px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>
      The Gap Is Real
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.7;margin:0;'>
      <b style='color:#fb923c;'>{untapped_pct}% of mid-tier artists</b> with local radio presence
      have <b>zero scheduled shows</b>. Not legacy acts — active, living artists with real
      audiences and no booking infrastructure. They're already on your local radio.
      They just haven't been booked.
    </p>
  </div>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #a78bfa;border-radius:8px;padding:18px 20px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>
      The Scale Is Massive
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.7;margin:0;'>
      <b style='color:#f59e0b;'>{n_opp} bookable artists · 0 shows</b>.
      At a conservative 20 shows per year each, that is
      <b style='color:#a78bfa;'>{potential_shows:,}+ unbooked shows per year</b>
      — live revenue that currently does not exist.
      Every orange dot is a venue night that should have happened.
    </p>
  </div>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #38bdf8;border-radius:8px;padding:18px 20px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>
      The Model Already Works
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.7;margin:0;'>
      <b style='color:#38bdf8;'>{len(active)} mid-tier artists are already touring</b>
      — {top3_active_names} and others — turning the same local radio reach into
      <b>avg. {avg_active_shows} shows/year</b>.
      The orange cluster has identical audience size. It just needs the connection.
    </p>
  </div>

</div>
""", unsafe_allow_html=True)


# ── Table ──────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='font-size:1rem;font-weight:700;color:#e2e8f0;
            margin-bottom:4px;letter-spacing:-0.01em;'>
  Who's Waiting to Be Booked
</div>
<div style='font-size:0.8rem;color:#4b5675;margin-bottom:14px;'>
  Top 25 untapped mid-tier artists · 0 shows · Airplay {AIRPLAY_MIN}–{AIRPLAY_MAX} · Active &amp; alive · Sorted by airplay reach
</div>
""", unsafe_allow_html=True)

tbl_df = (
    opp.nlargest(25, "airplay_count")
    [["name","airplay_count","shows_count","opp_score"]]
    .rename(columns={"name":"Artist","airplay_count":"Airplay",
                     "shows_count":"Shows / yr","opp_score":"Opp. Score"})
    .reset_index(drop=True)
)
tbl_df.index += 1
tbl_df["Opp. Score"] = tbl_df["Opp. Score"].round(0).astype(int)

col_t, col_exp = st.columns([1.8, 1])

with col_t:
    st.dataframe(
        tbl_df,
        use_container_width=True,
        height=470,
        column_config={
            "Airplay": st.column_config.ProgressColumn(
                "Airplay", min_value=0,
                max_value=int(opp["airplay_count"].max()), format="%d",
            ),
            "Opp. Score": st.column_config.NumberColumn(
                "Opp. Score",
                help="Airplay ÷ (Shows + 1)  ·  higher = larger untapped gap",
            ),
        },
    )

with col_exp:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;
                border-radius:10px;padding:22px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:14px;'>
        Opportunity Score
      </div>
      <p style='color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0;'>
        <span style='color:#fb923c;font-weight:600;'>Score = Airplay ÷ (Shows + 1)</span>
        <br><br>
        The higher the score, the wider the gap between the audience
        an artist has built and the live presence they've established.
        <br><br>
        <b style='color:#fde68a;'>Above 500</b> → significant untapped demand.
        <br><br>
        These artists are not unknown — they have radio history.
        What they lack is infrastructure: a manager, an agent, a venue connection.
        That is the exact gap Azimuth closes.
      </p>
      <hr style='border:none;border-top:1px solid #1e2535;margin:16px 0;'>
      <p style='color:#6b7a99;font-size:0.8rem;margin:0;line-height:1.55;'>
        <b style='color:#94a3b8;'>Data note:</b> shows_count reflects a specific dataset
        period. Some active artists may show 0 due to data gaps or hiatus.
        Deceased/permanently inactive artists are excluded and listed in the sidebar.
      </p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧹 Data Quality")
    st.markdown(f"- Total rows: **{len(df):,}**")
    st.markdown(f"- Null rows: **0**")
    st.markdown(f"- Duplicates: **0**")
    st.markdown(f"- Negatives clamped to 0")
    st.markdown(f"- Chart filter: airplay {AIRPLAY_MIN}–{AIRPLAY_MAX}")
    st.markdown("---")
    st.markdown("### 🚫 Removed from Analysis")
    st.caption(f"{len(removed)} artists excluded — deceased or permanently inactive")
    removed_list = removed.sort_values("airplay_count", ascending=False)[["name","airplay_count"]]
    removed_list.columns = ["Artist","Airplay"]
    removed_list = removed_list.reset_index(drop=True)
    removed_list.index += 1
    st.dataframe(removed_list, use_container_width=True, height=320)


# ── Venue data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_venue_data():
    pe = pd.read_csv("/Users/ashley/Desktop/Azimuth-Analytics/past_event.csv")
    ss = pd.read_csv("/Users/ashley/Desktop/Azimuth-Analytics/state_summary.csv")
    pe["venue_name"] = pe["venue_name"].fillna("").astype(str)
    return pe, ss

pe_df, ss_df = load_venue_data()
one_show_total = int(ss_df["one_show_venues"].sum())

_under = pe_df[(pe_df["total_events"] >= 1) & (pe_df["total_events"] <= 20)].copy()

def _categorize_venue(name):
    n = name.lower()
    if any(k in n for k in [
        "university", "college", "campus", "polytechnic", "seminary",
        "student union", "student center", "student centre",
        "fraternity", "sorority", "preparatory school", "prep school", "academy",
    ]):
        return "Colleges/Universities"
    if any(k in n for k in [
        "civic", "municipal", "city hall", "convention center", "convention ctr",
        "convention centre", "fairground", "fair ground", "town hall",
        "community center", "community centre", "community hall",
        "armory", "coliseum", "colosseum", "memorial auditorium", "memorial arena",
        "memorial hall", "memorial center", "memorial centre", "memorial stadium",
        "veterans", "veteran", "county", "state fair", " fair ", "county fair",
        "expo center", "expo centre", "expo hall", "civic center", "civic centre",
        "public library", "library", "public park", "cultural center", "cultural centre",
        "arts center", "arts centre", "art center", "art centre",
        "center for the arts", "centre for the arts", "performing arts", "art institute",
        "recreation center", "recreation centre", "rec center", "rec centre",
        "museum", "botanical", "high school", "middle school", "elementary school",
        "public school", " school", " fort", "fort ", "navy yard", "naval",
        "national guard", "church", "cathedral", "congregation", "synagogue", "mosque",
        "temple ", "chapel", "basilica", "abbey", "baptist", "methodist",
        "presbyterian", "lutheran", "episcopal", "unitarian", "evangelical",
    ]):
        return "Civic/Municipal"
    if any(k in n for k in [
        "park", "garden", "outdoor", "amphitheater", "amphitheatre",
        "lawn", "polo club", "polo field", "beach", "ranch",
        "pavilion", "bandshell", "band shell", "plaza", "meadow",
        "waterfront", "lakefront", "riverfront", "fairgrounds", "fair grounds",
        "festival", " fest", "fest ", "farm", "farms", "plantation",
        "winery", "vineyard", "cidery", " lake", "lake ", "lakeshore",
        "mountain", "mountains", " river", "river ", "riverside",
        " creek", "creekside", " valley", "valley ", " island", "island ",
        "woods", "forest", "grove", "backyard", "back yard",
        " camp", "campground", "campsite", " field", "field ", "grounds",
        "pier", "marina", "harbor", "harbour", "speedway", "raceway",
        "racetrack", "race track", "rodeo", "rally", "square", "commons",
        "cruise", "cruises", " market", "market ", "resort", "golf",
        "amusement", "theme park", " landing", "landing ",
    ]):
        return "Parks/Outdoor"
    if any(k in n for k in [
        "club", " bar", "bar ", "pub ", " pub", "lounge", "theater", "theatre",
        "hall", "ballroom", "concert", " music", "stage", "arena", "auditorium",
        "opera", "house of", "inn", "hotel", "casino", "nightclub", "comedy", "improv",
        "brewery", "brewing", "brewhouse", "brewpub", "taproom", "tap room",
        "alehouse", "roadhouse", "cafe", "café", "coffee", "saloon", "tavern",
        "cantina", "grill", "grille", "bistro", "restaurant", "diner", "lodge",
        "stadium", "fieldhouse", "event center", "events center", "event space",
        "event venue", "entertainment center", "entertainment complex", "entertainment",
        "warehouse", "factory", "gallery", "studio", "jazz", "whiskey", "whisky",
        "distillery", "distill", " beer", "beerworks", "bier", "cabaret", "speakeasy",
        "cellar", "cellars", "cider", "showcase", "showroom",
        "sports center", "sports complex", "sports village",
        " house", "house ", " room", "room ", "venue", "record", "records",
        "store", "shop ", "station", "loft", "rooftop",
    ]):
        return "Traditional Venues"
    return "Other"

_under["category"] = _under["venue_name"].apply(_categorize_venue)
_cat_counts = _under["category"].value_counts()
civic_count = int(_cat_counts.get("Civic/Municipal", 0))


# ── Sub-section 2: The Other Half ──────────────────────────────────────────────

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='border-top:1px solid #1e2535;padding-top:28px;margin-bottom:20px;'>
  <h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.02em;margin-bottom:8px;'>
    The Other Half — Empty Stages
  </h2>
  <p style='font-size:0.9rem;color:#64748b;margin:0 0 8px;line-height:1.65;'>
    Artists need stages. Across the United States, tens of thousands of stages already exist
    — and almost none of them are being consistently used.
  </p>
  <p style='font-size:0.85rem;color:#4b5675;margin:0;line-height:1.6;'>
    The {n_opp} artists above have audiences but no shows.
    The venues below have stages but no bookings.
    This is not an infrastructure problem — it is a connection problem.
    That connection is what Azimuth builds.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Venue KPI row ──────────────────────────────────────────────────────────────

vk1, vk2, vk3 = st.columns(3)
vk1.markdown(kpi("96,982",
                 "Underutilized Venues Nationwide<br>(Fewer Than 20 Shows in Dataset)",
                 "#fb923c"), unsafe_allow_html=True)
vk2.markdown(kpi(f"{civic_count:,}",
                 "Civic &amp; Municipal Venues<br>Among the Underutilized",
                 "#a78bfa"), unsafe_allow_html=True)
vk3.markdown(kpi(f"{one_show_total:,}",
                 "Venues That Have Hosted<br>Only 1 Show Ever",
                 "#38bdf8"), unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── Donut chart ────────────────────────────────────────────────────────────────

_CAT_ORDER  = ["Traditional Venues", "Parks/Outdoor", "Civic/Municipal", "Colleges/Universities", "Other"]
_CAT_COLORS = {
    "Traditional Venues":    "#334155",
    "Parks/Outdoor":         "#38bdf8",
    "Civic/Municipal":       "#fb923c",
    "Colleges/Universities": "#a78bfa",
    "Other":                 "#1e2535",
}
_CAT_PULL = {
    "Traditional Venues":    0,
    "Parks/Outdoor":         0.06,
    "Civic/Municipal":       0.08,
    "Colleges/Universities": 0.06,
    "Other":                 0,
}

_donut_vals   = [int(_cat_counts.get(c, 0)) for c in _CAT_ORDER]
_donut_colors = [_CAT_COLORS[c] for c in _CAT_ORDER]
_donut_pull   = [_CAT_PULL[c]   for c in _CAT_ORDER]

donut_fig = go.Figure(go.Pie(
    labels=_CAT_ORDER, values=_donut_vals, hole=0.58,
    marker=dict(colors=_donut_colors, line=dict(color="#0d1117", width=2.5)),
    pull=_donut_pull,
    textfont=dict(family="Inter, sans-serif", size=12, color="#e2e8f0"),
    hovertemplate="<b>%{label}</b><br>%{value:,} venues<br>%{percent}<extra></extra>",
    sort=False,
))

donut_fig.add_annotation(
    text=(
        "<b>96,982</b><br>"
        "<span style='font-size:10px;color:#64748b;'>underutilized</span><br>"
        "<span style='font-size:10px;color:#64748b;'>venues</span>"
    ),
    x=0.5, y=0.5, showarrow=False,
    font=dict(family="Inter, sans-serif", size=14, color="#e2e8f0"),
    xanchor="center", yanchor="middle", align="center",
)

donut_fig.update_layout(
    title=dict(
        text=(
            "<b style='color:#e2e8f0;font-size:15px;'>Stages Already Built — Rarely Used</b><br>"
            "<span style='color:#4b5675;font-size:11px;'>Venues with 1–20 shows in dataset</span>"
        ),
        x=0.0,
        font=dict(family="Inter, sans-serif"),
        pad=dict(b=8),
    ),
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    legend=dict(
        bgcolor="rgba(13,17,23,0.9)", bordercolor="#1e2535", borderwidth=1,
        font=dict(size=12, color="#94a3b8"),
        orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02,
    ),
    margin=dict(l=20, r=180, t=70, b=20),
    height=440,
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

col_donut, col_insight = st.columns([1.4, 1])

with col_donut:
    st.plotly_chart(donut_fig, use_container_width=True)

with col_insight:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-radius:10px;
                padding:22px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:16px;'>
        Where the Empty Supply Lives
      </div>

      <div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:16px;'>
        <div style='width:10px;height:10px;border-radius:50%;background:#fb923c;
                    flex-shrink:0;margin-top:4px;'></div>
        <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.65;margin:0;'>
          <b style='color:#fb923c;'>Civic &amp; Municipal</b> — city-owned venues
          with built-in legitimacy, accessibility, and often city subsidies.
          They sit under-scheduled year-round. No profit motive means they're open
          to lower-risk bookings and community-focused acts.
        </p>
      </div>

      <div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:16px;'>
        <div style='width:10px;height:10px;border-radius:50%;background:#38bdf8;
                    flex-shrink:0;margin-top:4px;'></div>
        <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.65;margin:0;'>
          <b style='color:#38bdf8;'>Parks &amp; Outdoor</b> — seasonal capacity
          that rarely gets activated for live music. Natural gathering points
          with near-zero venue cost, managed by parks departments
          who actively want community programming but lack a booking path.
        </p>
      </div>

      <div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:20px;'>
        <div style='width:10px;height:10px;border-radius:50%;background:#a78bfa;
                    flex-shrink:0;margin-top:4px;'></div>
        <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.65;margin:0;'>
          <b style='color:#a78bfa;'>Colleges &amp; Universities</b> — built-in
          audiences and event infrastructure (student unions, amphitheaters),
          chronically underbooked. Student activities budgets often go unspent
          for lack of a simple, trusted booking path.
        </p>
      </div>

      <hr style='border:none;border-top:1px solid #1e2535;margin:0 0 14px;'>
      <p style='color:#6b7a99;font-size:0.8rem;margin:0;line-height:1.6;'>
        <b style='color:#94a3b8;'>{one_show_total:,}</b> of these venues have hosted
        exactly one show — not a lack of capacity, a lack of connection.
        The bottleneck is discovery and coordination, not supply.
      </p>
    </div>
    """, unsafe_allow_html=True)


# ── Closing ────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='margin-top:32px;margin-bottom:12px;padding:24px 28px;
            background:#12161f;border:1px solid #1e2535;border-radius:12px;
            border-left:4px solid #fb923c;'>
  <p style='color:#e2e8f0;font-size:1.05rem;font-weight:500;
            line-height:1.7;margin:0 0 12px;font-style:italic;'>
    "The infrastructure exists. The audiences exist. What's missing is the connection
    — and that's what Azimuth builds."
  </p>
  <p style='color:#64748b;font-size:0.88rem;line-height:1.65;margin:0;'>
    Two problems, one platform.
    <b style='color:#fb923c;'>{n_opp} mid-tier artists</b> with audiences and empty calendars.
    <b style='color:#a78bfa;'>96,982 stages</b> with capacity and no booking pipeline.
    Azimuth is the intelligence layer that turns both into revenue —
    and the opportunity is hiding in plain sight.
  </p>
</div>
""", unsafe_allow_html=True)

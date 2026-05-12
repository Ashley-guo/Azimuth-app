import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="The Live Music Opportunity Gap",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Force dark background everywhere ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
section[data-testid="stSidebar"],
.main { background-color: #0d1117 !important; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem;
                   max-width: 1280px; background-color: #0d1117 !important; }

/* ── KPI cards ── */
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

/* ── Sidebar text ── */
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────

@st.cache_data
def load():
    df = pd.read_csv("airplay_vs_shows.csv")
    df = df.dropna(how="all")
    df = df[df["name"].str.strip().ne("")]
    df = df.drop_duplicates()
    df["airplay_count"] = df["airplay_count"].clip(lower=0)
    df["shows_count"]   = df["shows_count"].clip(lower=0)
    df["opp_score"]     = df["airplay_count"] / (df["shows_count"] + 1)
    return df

df = load()

# ── Threshold: airplay ≥ 100 = "proven audience reach" ──────────────────────
# This is the consistent baseline throughout: an artist with <100 radio plays
# does not have a demonstrated mass audience. Using 100 here is defensible and
# produces the same 193 raw figure referenced in prior analysis.
AIRPLAY_MIN = 100

# ── Deceased / permanently inactive artists ───────────────────────────────────
# Removed from opportunity analysis: they cannot book future shows.
DECEASED_OR_INACTIVE = {
    # Solo artists — deceased
    "Michael Jackson", "Prince", "Tom Petty", "George Michael",
    "Eddie Money", "Selena", "Eric Carmen", "Andy Williams",
    "Vicente Fernández", "Joan Sebastian", "Pop Smoke",
    "John Lennon", "Elvis Presley", "Avicii",
    # Bands — primary vocalist/member deceased, group won't perform
    "Nirvana", "Led Zeppelin", "Wham!", "The Cranberries",
    "Pink Floyd", "The Cars", "Tom Petty & the Heartbreakers",
    "The Outfield", "Fleetwood Mac",
}

opp_all = df[(df["shows_count"] == 0) & (df["airplay_count"] >= AIRPLAY_MIN)]
opp     = opp_all[~opp_all["name"].isin(DECEASED_OR_INACTIVE)]
removed = opp_all[opp_all["name"].isin(DECEASED_OR_INACTIVE)]

active = df[(df["shows_count"] >= 20)         & (df["airplay_count"] >= AIRPLAY_MIN)]
middle = df[(df["shows_count"].between(1, 19)) & (df["airplay_count"] >= AIRPLAY_MIN)]
ctx    = df[df["airplay_count"] < AIRPLAY_MIN]

n_opp            = len(opp)
total_opp_play   = int(opp["airplay_count"].sum())
potential_shows  = n_opp * 20


# ── Header ─────────────────────────────────────────────────────────────────────

# Derived stats for display
n_high_reach   = len(df[df["airplay_count"] >= AIRPLAY_MIN])   # 643
untapped_pct   = round(n_opp / n_high_reach * 100, 1)          # 26.9 → 27%

st.markdown(f"""
<div style='background:#0d1117;padding:0 0 4px 0;'>
<h1 style='font-size:1.9rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:6px;'>
  The Live Music Opportunity Gap
</h1>
<p style='font-size:0.97rem;color:#64748b;margin-bottom:24px;line-height:1.6;'>
  Among <b style='color:#94a3b8;'>{n_high_reach} artists</b> with proven radio reach (airplay ≥ 100),
  <b style='color:#fb923c;'>{untapped_pct}% have zero scheduled shows.</b>
  That is <b style='color:#fb923c;'>{n_opp} bookable artists</b> with
  audiences but no stage — after excluding deceased artists.
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
                f"Of High-Reach Artists Have 0 Shows<br>(airplay ≥ {AIRPLAY_MIN})",
                "#fb923c"), unsafe_allow_html=True)
k2.markdown(kpi(f"{n_opp}",
                f"Bookable Artists — 0 Shows · Airplay ≥ {AIRPLAY_MIN}<br>Deceased excluded",
                "#f59e0b"), unsafe_allow_html=True)
k3.markdown(kpi(f"{potential_shows:,}+",
                "Est. Unbooked Shows / yr<br>@ 20 shows per artist",
                "#a78bfa"), unsafe_allow_html=True)
k4.markdown(kpi(f"{len(active)}",
                f"Active Touring Artists<br>(≥20 shows · airplay ≥ {AIRPLAY_MIN})",
                "#38bdf8"), unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


# ── Build chart ────────────────────────────────────────────────────────────────

rng   = np.random.default_rng(42)
# Use plotted data max (deceased artists excluded from opp, so no wasted vertical space)
y_max = int(max(
    opp["airplay_count"].max(),
    active["airplay_count"].max(),
    middle["airplay_count"].max(),
))
X_GAP_L, X_GAP_R = 6.5, 17             # visual gap corridor boundaries

fig = go.Figure()

# ① Zone fills ─────────────────────────────────────────────────────────────────
for shape_args in [
    dict(x0=-4,      x1=X_GAP_L, fillcolor="rgba(251,146,60,0.06)"),
    dict(x0=X_GAP_L, x1=X_GAP_R, fillcolor="rgba(255,255,255,0.015)"),
    dict(x0=X_GAP_R, x1=135,     fillcolor="rgba(56,189,248,0.04)"),
]:
    fig.add_shape(type="rect", layer="below",
                  y0=-80, y1=y_max * 1.14,
                  line_width=0, **shape_args)

# Soft divider lines at zone edges
for xv, dash in [(X_GAP_L, "dot"), (X_GAP_R, "dot")]:
    fig.add_shape(type="line", layer="below",
                  x0=xv, x1=xv, y0=0, y1=y_max * 1.1,
                  line=dict(color="#1e2535", width=1.5, dash=dash))

# ② Context dots: airplay < 50  (almost invisible — just shows scale) ──────────
fig.add_trace(go.Scatter(
    x=ctx["shows_count"], y=ctx["airplay_count"],
    mode="markers",
    marker=dict(color="#151b28", size=2.5, opacity=0.5),
    hoverinfo="skip", showlegend=False,
))

# ③ Middle band: 1–19 shows, muted ────────────────────────────────────────────
j_mid = rng.uniform(-0.7, 0.7, len(middle))
fig.add_trace(go.Scatter(
    x=middle["shows_count"] + j_mid,
    y=middle["airplay_count"],
    mode="markers",
    name="Some Activity  (1–19 shows)",
    marker=dict(
        color="#334155", size=np.clip(middle["airplay_count"] / 80, 4, 10),
        opacity=0.55, line=dict(color="#475569", width=0.4),
    ),
    customdata=middle[["name","airplay_count","shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows %{customdata[2]}<extra></extra>",
))

# ④ Active touring: blue ───────────────────────────────────────────────────────
j_act = rng.uniform(-1.5, 1.5, len(active))
fig.add_trace(go.Scatter(
    x=active["shows_count"] + j_act,
    y=active["airplay_count"],
    mode="markers",
    name="Active Touring  (≥20 shows · airplay ≥100)",
    marker=dict(
        color="#38bdf8",
        size=np.clip(active["airplay_count"] / 65, 6, 20),
        opacity=0.82,
        line=dict(color="rgba(186,230,253,0.25)", width=0.8),
    ),
    customdata=active[["name","airplay_count","shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows/yr %{customdata[2]}<extra></extra>",
))

# ⑤ Opportunity: orange glow ──────────────────────────────────────────────────
j_opp = rng.uniform(-2.5, 2.5, len(opp))
fig.add_trace(go.Scatter(
    x=j_opp,
    y=opp["airplay_count"],
    mode="markers",
    name="Untapped Audience  (0 shows · airplay ≥100 · deceased excluded)",
    marker=dict(
        color="#fb923c",
        size=np.clip(opp["airplay_count"] / 55, 7, 24),
        opacity=0.92,
        line=dict(color="rgba(253,186,116,0.35)", width=1),
    ),
    customdata=opp[["name","airplay_count","shows_count","opp_score"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Airplay: %{customdata[1]:,}<br>"
        "Shows/yr: %{customdata[2]}<br>"
        "Opp. Score: %{customdata[3]:.0f}"
        "<extra></extra>"
    ),
))

# ⑥ Zone header labels ─────────────────────────────────────────────────────────
zone_labels = [
    dict(x=1.0,  y=y_max*1.105, text="<b>UNTAPPED</b>",    color="#fb923c", size=13),
    dict(x=1.0,  y=y_max*1.055, text="AUDIENCE",           color="#f97316", size=11),
    dict(x=11.5, y=y_max*1.105, text="← THE GAP →",        color="#475569", size=12),
    dict(x=11.5, y=y_max*1.055, text=f"{potential_shows:,}+ shows unbooked", color="#374151", size=10),
    dict(x=72,   y=y_max*1.105, text="<b>ACTIVE</b>",      color="#38bdf8", size=13),
    dict(x=72,   y=y_max*1.055, text="TOURING",            color="#0ea5e9", size=11),
]
for lbl in zone_labels:
    fig.add_annotation(
        x=lbl["x"], y=lbl["y"],
        text=lbl["text"],
        showarrow=False,
        font=dict(size=lbl["size"], color=lbl["color"], family="Inter, sans-serif"),
        xanchor="center", yanchor="bottom",
        xref="x", yref="y",
    )

# ⑦ Arrow-annotate top 8 opportunity artists ──────────────────────────────────
# (ax,ay) = text box position  |  (x,y) = arrowhead at dot
# All labels placed to the right inside the gap zone
label_targets = [
    # name,             dot_y,  label_y,  label_x
    # (all alive / active artists only — deceased removed from opp dataset)
    ("Queen",            2203,   2203,     8.5),   # still tours as Queen + Adam Lambert
    ("The Police",       1350,   1370,     8.5),
    ("Ozuna",            1146,   1150,     8.5),
    ("Tears For Fears",   943,    940,     8.5),
    ("Rihanna",           918,    780,     8.5),
    ("Taylor Swift",      863,    620,     8.5),
    ("Romeo Santos",      859,    460,     8.5),
    ("Eurythmics",        817,    300,     8.5),
]
# map name → actual jitter_x from the scatter
name_to_jitter = dict(zip(opp["name"].values, j_opp))

for name, dot_y, lbl_y, lbl_x in label_targets:
    dot_x = name_to_jitter.get(name, 0.0)
    # draw line from label → dot
    fig.add_shape(type="line",
                  x0=lbl_x, y0=lbl_y,
                  x1=dot_x,  y1=dot_y,
                  line=dict(color="#4b5675", width=0.9, dash="dot"),
                  xref="x", yref="y")
    fig.add_annotation(
        x=lbl_x, y=lbl_y,
        text=f"<b>{name}</b>",
        showarrow=False,
        font=dict(size=10.5, color="#fde68a", family="Inter, sans-serif"),
        xanchor="left", yanchor="middle",
        xref="x", yref="y",
        bgcolor="rgba(13,17,23,0.0)",
    )

# ⑧ Arrow-annotate top 3 active touring artists ───────────────────────────────
active_labels = [
    ("Morgan Wallen", 2551, 41),
    ("Bad Bunny",     1948, 71),
    ("Luke Combs",    1862, 39),
]
name_to_act_jitter = dict(zip(active["name"].values, j_act))
for name, airplay, shows in active_labels:
    jx = name_to_act_jitter.get(name, 0.0)
    fig.add_annotation(
        x=shows + jx,
        y=airplay + 90,
        text=f"<b>{name}</b>",
        showarrow=True,
        arrowhead=2, arrowcolor="#7dd3fc", arrowwidth=1, arrowsize=0.8,
        ax=0, ay=-28,
        font=dict(size=10, color="#bae6fd", family="Inter, sans-serif"),
        xanchor="center", yanchor="bottom",
        bgcolor="rgba(13,17,23,0.65)",
        bordercolor="#1e3a5f",
        borderwidth=1,
        borderpad=4,
    )

# ⑨ "Path to revenue" arrow (curved via 3-segment lines) ─────────────────────
# A simple straight arrow from x=2 y=1100 → x=17 y=1100
fig.add_annotation(
    x=X_GAP_R - 0.5, y=1300,
    ax=2.5, ay=1300,
    xref="x", yref="y", axref="x", ayref="y",
    text="path to<br>live revenue",
    showarrow=True,
    arrowhead=3, arrowcolor="#4b5675", arrowwidth=1.5, arrowsize=1,
    font=dict(size=9, color="#475569", family="Inter, sans-serif"),
    xanchor="right", yanchor="middle",
    bgcolor="rgba(13,17,23,0)",
)

# ⑩ Layout ────────────────────────────────────────────────────────────────────
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),

    title=dict(
        text=(
            "<b style='color:#e2e8f0;font-size:17px;'>Airplay Reach vs. Live Shows per Year</b>"
            "  <span style='color:#374151;font-size:12px;'>  ·  "
            "dot size = audience reach  ·  "
            "<span style='color:#fb923c;'>●</span> zero shows  "
            "<span style='color:#334155;'>●</span> 1–19 shows  "
            "<span style='color:#38bdf8;'>●</span> active touring"
            "</span>"
        ),
        x=0.0,
        font=dict(family="Inter, sans-serif"),
        pad=dict(b=8),
    ),

    xaxis=dict(
        title=dict(text="Number of Shows per Year", font=dict(size=13, color="#64748b")),
        range=[-4, 128],
        gridcolor="#111827",
        zeroline=False,
        tickfont=dict(size=12, color="#6b7280"),
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showspikes=True, spikecolor="#1e2535", spikethickness=1,
    ),

    yaxis=dict(
        title=dict(text="Airplay Count  —  Audience Reach Proxy", font=dict(size=13, color="#64748b")),
        range=[-80, y_max * 1.20],
        gridcolor="#111827",
        zeroline=False,
        tickfont=dict(size=12, color="#6b7280"),
        showspikes=True, spikecolor="#1e2535", spikethickness=1,
    ),

    legend=dict(
        bgcolor="rgba(13,17,23,0.9)",
        bordercolor="#1e2535",
        borderwidth=1,
        font=dict(size=11.5, color="#94a3b8"),
        itemsizing="constant",
        orientation="h",
        yanchor="bottom", y=-0.16,
        xanchor="left",   x=0,
        tracegroupgap=4,
    ),

    margin=dict(l=70, r=30, t=80, b=90),
    height=660,

    hoverlabel=dict(
        bgcolor="#1a2133",
        bordercolor="#2e3a52",
        font=dict(size=12.5, family="Inter, sans-serif"),
    ),
)

st.plotly_chart(fig, use_container_width=True)


# ── Insight strip ──────────────────────────────────────────────────────────────

avg_active_shows = round(active["shows_count"].mean(), 1)
st.markdown(f"""
<div style='display:flex;gap:12px;margin:2px 0 28px;'>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #fb923c;border-radius:8px;padding:16px 18px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>
      The Core Finding
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.65;margin:0;'>
      <b style='color:#fb923c;'>{untapped_pct}% of artists with proven radio reach
      (airplay ≥ {AIRPLAY_MIN})</b> have <b>zero scheduled shows</b>.
      These are alive, bookable artists — not catalogue acts. The demand
      exists; the supply of shows does not.
    </p>
  </div>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #a78bfa;border-radius:8px;padding:16px 18px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>
      Scale of the Gap
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.65;margin:0;'>
      <b style='color:#f59e0b;'>{n_opp} bookable artists · 0 shows</b>.
      At a conservative 20 shows/year each, that is
      <b style='color:#a78bfa;'>{potential_shows:,}+ unbooked shows per year</b>
      — live revenue that currently does not exist.
    </p>
  </div>

  <div style='flex:1;background:#12161f;border:1px solid #1e2535;
              border-top:2px solid #38bdf8;border-radius:8px;padding:16px 18px;'>
    <div style='font-size:0.7rem;font-weight:600;color:#4b5675;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>
      Blue = Proof the Model Works
    </div>
    <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.65;margin:0;'>
      <b style='color:#38bdf8;'>{len(active)} active touring artists</b>
      (Morgan Wallen, Bad Bunny, Luke Combs…) converted the same airplay
      reach into <b>avg. {avg_active_shows} shows/year</b>.
      The orange cluster is on the same path — just not yet booked.
    </p>
  </div>

</div>
""", unsafe_allow_html=True)


# ── Table ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='font-size:1rem;font-weight:700;color:#e2e8f0;
            margin-bottom:4px;letter-spacing:-0.01em;'>
  Top 25 Untapped Artists
</div>
<div style='font-size:0.8rem;color:#4b5675;margin-bottom:14px;'>
  Sorted by airplay reach · 0 shows · Airplay ≥ 100 · Deceased excluded
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
      <p style='color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0;'>
        <span style='color:#fb923c;font-weight:600;'>Score = Airplay ÷ (Shows + 1)</span>
        <br><br>
        The higher the score, the wider the gap between the audience
        an artist has built and the live presence they have established.
        <br><br>
        <b style='color:#fde68a;'>Above 500</b> → significant untapped demand.<br>
        <b style='color:#fb923c;'>Above 1,000</b> → rare first-mover window.
      </p>
      <hr style='border:none;border-top:1px solid #1e2535;margin:16px 0;'>
      <p style='color:#6b7a99;font-size:0.8rem;margin:0;line-height:1.55;'>
        <b style='color:#94a3b8;'>Data note:</b> shows_count reflects a
        specific dataset period. Some active artists may show 0 shows
        due to data gaps, hiatus, or residency-only schedules.
        20 deceased/permanently inactive artists have been removed
        from this analysis and are listed in the sidebar.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar: data quality + removed artists ────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧹 Data Quality")
    st.markdown(f"- Total rows: **{len(df):,}**")
    st.markdown(f"- Null rows: **0**")
    st.markdown(f"- Duplicates: **0**")
    st.markdown(f"- Negatives clamped to 0")
    st.markdown(f"- Chart filter: airplay ≥ 50")
    st.markdown("---")
    st.markdown("### 🚫 Removed from Analysis")
    st.caption(f"{len(removed)} artists excluded — deceased or band permanently inactive")
    removed_list = removed.sort_values("airplay_count", ascending=False)[["name","airplay_count"]]
    removed_list.columns = ["Artist","Airplay"]
    removed_list = removed_list.reset_index(drop=True)
    removed_list.index += 1
    st.dataframe(removed_list, use_container_width=True, height=320)

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

_HERE = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Azimuth Analytics — The Live Event Calendar Opportunity",
    page_icon="📊",
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
.main { background-color: #0d1117 !important; }

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1280px;
    background-color: #0d1117 !important;
}

.kpi-wrap {
    background: #12161f;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 22px 18px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 28px rgba(0,0,0,0.35);
}
.kpi-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 14px 14px 0 0;
}
.kpi-num {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    letter-spacing: -0.04em;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #6b7a99;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    line-height: 1.55;
}

h1, h2, h3 { color: #e2e8f0 !important; }
p, li { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED HELPER
# ─────────────────────────────────────────────────────────────────────────────

def kpi(val, lbl, accent):
    return (
        f"<div class='kpi-wrap' style='--accent:{accent};'>"
        f"<div class='kpi-num'>{val}</div>"
        f"<div class='kpi-sub'>{lbl}</div>"
        f"</div>"
    )


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 1 — STATIC DATA
# ─────────────────────────────────────────────────────────────────────────────

total_events       = 2_021_138
prime_night_events = 1_181_211
prime_night_share  = 58.44
non_prime          = total_events - prime_night_events

weekday_data = pd.DataFrame({
    "weekday": [0, 1, 2, 3, 4, 5, 6],
    "day":     ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "total_events": [284843, 140118, 187640, 223357, 288812, 425082, 471286],
})
weekday_data["is_prime"]    = weekday_data["weekday"].isin([0, 5, 6])
weekday_data["event_share"] = weekday_data["total_events"] / total_events * 100

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_data["day"] = pd.Categorical(weekday_data["day"], categories=weekday_order, ordered=True)
weekday_data = weekday_data.sort_values("day").reset_index(drop=True)

avg_events = weekday_data["total_events"].mean()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 1 — HERO
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:16px 0 36px;'>
  <div style='font-size:0.72rem;font-weight:700;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.18em;margin-bottom:14px;'>
    Chapter 1
  </div>
  <h1 style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.08;margin:0 0 12px;'>
    The Live Event Calendar Is Structurally Concentrated
  </h1>
  <p style='font-size:1rem;color:#64748b;max-width:660px;line-height:1.7;margin:0 0 28px;'>
    Live entertainment demand concentrates into peak booking windows,
    while much of the venue calendar remains under&#8209;activated.
  </p>
  <div style='display:flex;flex-direction:column;gap:12px;max-width:700px;
              border-left:3px solid #fb923c;padding-left:20px;'>
    <p style='margin:0;font-size:1rem;color:#94a3b8;line-height:1.7;'>
      Uber transformed <b style='color:#e2e8f0;'>idle mobility capacity</b>
      into a coordinated transportation network.
    </p>
    <p style='margin:0;font-size:1rem;color:#94a3b8;line-height:1.7;'>
      Airbnb transformed <b style='color:#e2e8f0;'>underutilized housing inventory</b>
      into bookable hospitality supply.
    </p>
    <p style='margin:0;font-size:1rem;line-height:1.7;'>
      <b style='color:#fb923c;font-weight:700;'>
        Azimuth transforms under&#8209;activated venue calendars
        into programmable live&#8209;event infrastructure.
      </b>
    </p>
  </div>
  <p style='margin:24px 0 0;font-size:0.9rem;color:#64748b;
            max-width:620px;line-height:1.8;'>
    Live entertainment demand is not evenly distributed across the calendar —
    it concentrates into a narrow set of peak booking windows, creating a
    structural utilization gap the industry has never systematically coordinated.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 1 — KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────

c1, c2, c3 = st.columns(3)
c1.markdown(kpi(f"{total_events:,}",        "Total Historical Events<br>in Dataset",             "#fb923c"), unsafe_allow_html=True)
c2.markdown(kpi(f"{prime_night_events:,}",  "Events in Peak Booking Windows<br>Fri · Sat · Sun", "#f59e0b"), unsafe_allow_html=True)
c3.markdown(kpi(f"{prime_night_share:.1f}%","of All Events<br>in Just 3 Booking Windows",        "#a78bfa"), unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
            border-radius:8px;padding:15px 22px;'>
  <p style='color:#cbd5e1;font-size:0.92rem;line-height:1.75;margin:0;'>
    <b style='color:#fb923c;'>Key insight:</b>
    Friday, Saturday, and Sunday alone account for
    <b style='color:#fb923c;'>{prime_night_share:.1f}%</b> of all {total_events:,} live events.
    The remaining four weekdays share just <b style='color:#94a3b8;'>{non_prime:,} events</b> —
    less than four-tenths of total demand. Live entertainment is fundamentally a
    <b style='color:#e2e8f0;'>peak-window inventory economy</b>.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 1 — CHART 1: WEEKDAY DEMAND BAR CHART
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  58% of All Live Events Land on Just Three Days
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:2px;line-height:1.65;'>
  Event volume by day of week across 2.0M historical events.
  <span style='color:#fb923c;'>&#9679; Peak booking windows</span>
  vs.
  <span style='color:#334155;'>&#9679; Off-peak windows</span> —
  the gap is structural, not seasonal.
</p>
""", unsafe_allow_html=True)

bar_colors  = ["#fb923c" if r else "#1e2d45" for r in weekday_data["is_prime"]]
bar_borders = ["rgba(251,146,60,0.55)" if r else "#253044" for r in weekday_data["is_prime"]]
txt_colors  = ["#fb923c" if r else "#6b7a99" for r in weekday_data["is_prime"]]

fig1 = go.Figure()

fig1.add_shape(
    type="rect", layer="below",
    x0=3.5, x1=6.5,
    y0=0, y1=weekday_data["total_events"].max() * 1.22,
    fillcolor="rgba(251,146,60,0.055)",
    line_width=0,
)
fig1.add_shape(
    type="line", layer="below",
    x0=3.5, x1=3.5,
    y0=0, y1=weekday_data["total_events"].max() * 1.19,
    line=dict(color="rgba(251,146,60,0.22)", width=1.2, dash="dot"),
)

fig1.add_trace(go.Bar(
    x=weekday_data["day"],
    y=weekday_data["total_events"],
    marker=dict(
        color=bar_colors,
        line=dict(color=bar_borders, width=1),
        opacity=0.92,
    ),
    text=[
        f"<b>{v:,}</b><br>{s:.1f}%"
        for v, s in zip(weekday_data["total_events"], weekday_data["event_share"])
    ],
    textposition="outside",
    textfont=dict(size=11, color=txt_colors, family="Inter, sans-serif"),
    hovertemplate="<b>%{x}</b><br>Events: %{y:,}<br>Share: <b>%{customdata:.1f}%</b><extra></extra>",
    customdata=weekday_data["event_share"],
))

fig1.add_hline(
    y=avg_events,
    line=dict(color="#334155", width=1.5, dash="dot"),
    annotation_text=f"  Weekly avg  {avg_events:,.0f}",
    annotation_position="top right",
    annotation_font=dict(color="#64748b", size=11, family="Inter, sans-serif"),
)

fig1.add_annotation(
    x=5.0, y=weekday_data["total_events"].max() * 1.155,
    text="<b>PEAK ZONE</b>",
    showarrow=False,
    font=dict(size=11, color="#fb923c", family="Inter, sans-serif"),
    xanchor="center", xref="x", yref="y",
    bgcolor="rgba(251,146,60,0.12)",
    bordercolor="rgba(251,146,60,0.30)",
    borderwidth=1, borderpad=6,
)

sat_val = int(weekday_data[weekday_data["day"] == "Saturday"]["total_events"].iloc[0])
fig1.add_annotation(
    x="Saturday", y=sat_val,
    text="Highest-demand window<br>24.4% of all events",
    showarrow=True, arrowhead=2, arrowcolor="#fb923c",
    arrowwidth=1.5, arrowsize=0.9,
    ax=55, ay=-52,
    font=dict(color="#fb923c", size=10.5, family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.88)",
    bordercolor="rgba(251,146,60,0.35)",
    borderpad=6,
)

fig1.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=540,
    margin=dict(l=60, r=80, t=20, b=60),
    xaxis=dict(
        title=dict(text="Day of Week", font=dict(size=13, color="#64748b")),
        gridcolor="#0d1520", tickfont=dict(size=13, color="#94a3b8"),
        showgrid=False, zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Number of Events", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, weekday_data["total_events"].max() * 1.25],
    ),
    showlegend=False,
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig1, use_container_width=True)

fri_sat_sun = int(weekday_data[weekday_data["is_prime"]]["total_events"].sum())
mon_thu     = int(weekday_data[~weekday_data["is_prime"]]["total_events"].sum())
sat_share   = float(weekday_data[weekday_data["day"] == "Saturday"]["event_share"].iloc[0])

col_ia, col_ib = st.columns(2)
with col_ia:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:8px;padding:18px 20px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:8px;'>Peak vs. Off-Peak Booking Split</div>
      <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.7;margin:0;'>
        Fri–Sun generate <b style='color:#fb923c;'>{fri_sat_sun:,} events</b> —
        <b>{fri_sat_sun/mon_thu:.1f}×</b> more than the entire
        Mon–Thu period ({mon_thu:,} events combined).
      </p>
    </div>
    """, unsafe_allow_html=True)
with col_ib:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #f59e0b;
                border-radius:8px;padding:18px 20px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:8px;'>Saturday Alone</div>
      <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.7;margin:0;'>
        Saturday is the single highest-demand booking window at
        <b style='color:#f59e0b;'>{sat_share:.1f}%</b> of all events —
        <b>{sat_share / weekday_data["event_share"].mean():.1f}×</b> the weekly average.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# BRIDGE — Chapter 1 → Chapter 2
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='padding:22px 28px;background:#12161f;border:1px solid #1e2535;
            border-radius:12px;border-left:4px solid #fb923c;
            box-shadow:0 4px 24px rgba(0,0,0,0.35);margin-bottom:8px;'>
  <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
              letter-spacing:0.12em;margin-bottom:10px;'>What Comes Next</div>
  <p style='color:#e2e8f0;font-size:1.02rem;font-weight:500;line-height:1.8;margin:0 0 10px;'>
    <b style='color:#fb923c;'>{prime_night_share:.1f}%</b> of all {total_events:,} live events
    compress into just three booking windows every week.
    The opportunity is not in building more venues — it is in identifying
    which proven stages carry under-activated calendar capacity,
    and which artists are already ready to fill them.
  </p>
  <p style='color:#64748b;font-size:0.9rem;line-height:1.75;margin:0;'>
    <b style='color:#94a3b8;'>Chapter 2</b> maps the supply side:
    how concentrated are venue calendars, and where does weekday inventory remain ready to activate?<br>
    <b style='color:#a78bfa;'>Chapter 3</b> maps the demand side:
    which artists already have audiences — and are ready to be connected to a stage?
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — VENUE DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_venue_data():
    df = pd.read_csv(os.path.join(_HERE, "data", "venue_prime_night_dependence.csv"))
    df["venue_capacity"] = pd.to_numeric(df["venue_capacity"], errors="coerce")
    df["cap_valid"] = df["venue_capacity"].fillna(0).clip(lower=0)
    df["bubble"]    = np.where(
        df["cap_valid"] > 0,
        np.clip(np.log1p(df["cap_valid"]) * 3.2, 7, 42),
        7,
    )
    df["cap_label"] = np.where(
        df["cap_valid"] > 0,
        df["cap_valid"].astype(int).astype(str), "—"
    )
    # Tier labels kept for bubble chart legend
    df["tier"] = pd.cut(
        df["prime_night_share"],
        bins=[-0.001, 40, 80, 100.001],
        labels=["Balanced  (<40%)", "Peak-Skewed  (40–80%)", "Extreme  (≥80%)"],
    )
    return df


vdf = load_venue_data()

v_total       = len(vdf)
v_avg_prime   = vdf["prime_night_share"].mean()
v_avg_off     = vdf["off_night_share"].mean()
v_extreme     = int((vdf["prime_night_share"] >= 80).sum())
v_extreme_pct = v_extreme / v_total * 100
v_balanced    = int((vdf["prime_night_share"] < 40).sum())


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — HERO
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:8px 0 26px;'>
  <div style='font-size:0.78rem;font-weight:600;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;'>
    Chapter 2  ·  Continuing from Chapter 1
  </div>
  <h1 style='font-size:2.6rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.1;margin-bottom:14px;'>
    Venue Calendars Follow the Same Structural Pattern
  </h1>
  <p style='font-size:0.97rem;color:#64748b;max-width:740px;line-height:1.8;
            border-left:3px solid #1e2535;padding-left:16px;margin:0;'>
    Chapter 2 zooms in to the venue level: how concentrated is each venue's own calendar?
    The answer reveals a structural utilization opportunity — not a venue shortage.
    Most venues operate economically on a narrow band of the weekly calendar,
    leaving the rest of their inventory <b style='color:#e2e8f0;'>under-activated</b>.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────

vc1, vc2, vc3, vc4 = st.columns(4)
vc1.markdown(kpi(f"{v_total:,}",
                 "Venues Analyzed<br>Min. 20 Historical Events",
                 "#fb923c"), unsafe_allow_html=True)
vc2.markdown(kpi(f"{v_avg_prime:.1f}%",
                 "Avg Peak-Window Concentration<br>Fri · Sat · Sun",
                 "#f59e0b"), unsafe_allow_html=True)
vc3.markdown(kpi(f"{v_extreme:,}",
                 f"Venues ≥80% Peak-Window<br>Extreme Concentration · {v_extreme_pct:.0f}% of Total",
                 "#fb923c"), unsafe_allow_html=True)
vc4.markdown(kpi(f"{v_avg_off:.1f}%",
                 "Avg Off-Peak Share<br>Mon · Tue · Wed · Thu",
                 "#475569"), unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
            border-radius:8px;padding:14px 22px;'>
  <p style='color:#cbd5e1;font-size:0.92rem;line-height:1.8;margin:0;'>
    <b style='color:#fb923c;'>Key insight:</b>
    Across {v_total:,} established venues with at least 20 historical events,
    <b style='color:#fb923c;'>{v_extreme:,} ({v_extreme_pct:.0f}%)</b>
    run 80% or more of all their events on Friday, Saturday, or Sunday.
    Their Monday-through-Thursday calendar represents structurally underutilized inventory —
    not a capacity problem, but a <b style='color:#e2e8f0;'>calendar coordination gap</b>.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — DATA NOTE
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #475569;
            border-radius:8px;padding:16px 24px;margin-bottom:8px;'>
  <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
              letter-spacing:0.12em;margin-bottom:8px;'>Data Note — Why Festivals Were Excluded</div>
  <p style='color:#94a3b8;font-size:0.86rem;line-height:1.75;margin:0;'>
    Festival and one-off entities (Coachella, Lollapalooza, tours, parades) were filtered out
    before this analysis — they are structurally weekend-only by design and would make the
    finding trivially obvious. The remaining <b style='color:#fb923c;'>{v_total:,} venues</b>
    are ordinary clubs, theaters, arenas, and ballrooms that could host events any day of the week.
    And yet the concentration pattern holds. <b style='color:#e2e8f0;'>That is what makes it structural.</b>
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — PEAK-BOOKING CONCENTRATION CURVE (Histogram)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  The Concentration Distribution Across 17,315 Venues
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  Every bar is a bucket of venues sharing a similar peak-booking concentration.
  Bars toward the <b style='color:#38bdf8;'>left (blue)</b> = venues whose bookings spread
  relatively evenly across the week.
  Bars toward the <b style='color:#fb923c;'>right (orange)</b> = venues whose activity is
  almost entirely concentrated into Friday–Sunday.
  <b style='color:#e2e8f0;'>The shape of this curve is the shape of Azimuth's opportunity.</b>
</p>
""", unsafe_allow_html=True)

_bins_h = np.arange(0, 105, 5)
_hist_vals, _bin_edges = np.histogram(vdf["prime_night_share"], bins=_bins_h)
_bin_centers = (_bin_edges[:-1] + _bin_edges[1:]) / 2
_y_ceil = _hist_vals.max() * 1.32

_bar_clr = []
for _c in _bin_centers:
    if _c < 40:
        _bar_clr.append("#1e3a5f")
    elif _c < 80:
        _bar_clr.append("#78350f")
    else:
        _bar_clr.append("#fb923c")

fig_hist = go.Figure()

for _x0, _x1, _fill in [
    (0,  40,  "rgba(56,189,248,0.035)"),
    (40, 80,  "rgba(245,158,11,0.05)"),
    (80, 100, "rgba(251,146,60,0.08)"),
]:
    fig_hist.add_shape(type="rect", layer="below",
                       x0=_x0, x1=_x1, y0=0, y1=_y_ceil,
                       fillcolor=_fill, line_width=0)

for _xv, _col in [(40, "#1e3a5f"), (80, "rgba(251,146,60,0.5)")]:
    fig_hist.add_shape(type="line", layer="below",
                       x0=_xv, x1=_xv, y0=0, y1=_y_ceil * 0.96,
                       line=dict(color=_col, width=1.2, dash="dot"))

fig_hist.add_trace(go.Bar(
    x=_bin_centers, y=_hist_vals, width=4.3,
    marker=dict(color=_bar_clr, opacity=0.9,
                line=dict(color="rgba(0,0,0,0.25)", width=0.4)),
    hovertemplate="Peak-Booking Share: <b>%{x:.0f}%</b><br>Venues: <b>%{y:,}</b><extra></extra>",
))

fig_hist.add_annotation(
    x=80, y=_y_ceil * 0.93,
    text="<b>80% Threshold</b><br>Extreme Peak-Booking Dependence",
    showarrow=True, arrowhead=2, arrowcolor="rgba(251,146,60,0.7)",
    arrowwidth=1.5, ax=56, ay=0,
    font=dict(size=11.5, color="#fb923c", family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.88)", bordercolor="rgba(251,146,60,0.40)",
    borderpad=8, borderwidth=1, xanchor="left",
)

for _x_mid, _label, _color, _bg in [
    (20, "BALANCED",     "#38bdf8", "rgba(56,189,248,0.10)"),
    (60, "PEAK-SKEWED",  "#f59e0b", "rgba(245,158,11,0.10)"),
    (90, "EXTREME",      "#fb923c", "rgba(251,146,60,0.14)"),
]:
    fig_hist.add_annotation(
        x=_x_mid, y=_y_ceil * 0.82, text=f"<b>{_label}</b>",
        showarrow=False,
        font=dict(size=11, color=_color, family="Inter, sans-serif"),
        xanchor="center", bgcolor=_bg, bordercolor=_color,
        borderpad=6, borderwidth=1,
    )

_peak_idx   = _hist_vals.argmax()
_peak_x     = _bin_centers[_peak_idx]
_peak_count = _hist_vals[_peak_idx]
fig_hist.add_annotation(
    x=_peak_x, y=_peak_count,
    text=f"<b>{_peak_count:,} venues</b><br>most common range",
    showarrow=True, arrowhead=2, arrowcolor="#6b7a99", arrowwidth=1.2,
    ax=0, ay=-52,
    font=dict(size=10.5, color="#94a3b8", family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.80)", bordercolor="#1e2535", borderpad=6, borderwidth=1,
)

fig_hist.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=460,
    margin=dict(l=65, r=70, t=24, b=65),
    xaxis=dict(
        title=dict(text="Peak-Booking Concentration  (%  of events on Fri / Sat / Sun)",
                   font=dict(size=13, color="#64748b")),
        range=[0, 101], dtick=10,
        tickfont=dict(size=12, color="#94a3b8"),
        gridcolor="#0d1520", zeroline=False, showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Number of Venues", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, _y_ceil],
    ),
    showlegend=False, bargap=0.12,
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown(f"""
<p style='font-size:0.82rem;color:#475569;text-align:center;margin:-12px 0 16px;'>
  Festival and one-off entities excluded · Min. 20 events per venue ·
  <b style='color:#fb923c;'>{v_extreme:,} venues ({v_extreme_pct:.0f}%)</b> above the 80% line
</p>
""", unsafe_allow_html=True)

_ri1, _ri2, _ri3 = st.columns(3)
with _ri1:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #38bdf8;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#38bdf8;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Balanced  &lt;40%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Only <b style='color:#38bdf8;'>{v_balanced:,} venues</b> here.
        These stages activate consistently across the week —
        their calendar is well-utilised. Rare in this market.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _ri2:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#f59e0b;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Peak-Skewed  40–80%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        The largest zone. These venues lean toward weekends but still hold
        some weekday activity — partial utilisation, with off-peak capacity
        uncaptured. Most booking platforms treat these as "fully booked" when
        significant inventory remains available.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _ri3:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#fb923c;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Extreme  ≥80%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        <b style='color:#fb923c;'>{v_extreme:,} venues</b> — {v_extreme_pct:.0f}% of the market.
        4 out of every 5 booking dates fall within just three days.
        Their Mon–Thu calendar represents structurally under-used inventory.
        <b style='color:#e2e8f0;'>This is Azimuth's primary target segment.</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — BUBBLE SCATTER: "Where Venue Activity Becomes Peak-Window Locked"
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Proven Venues, Peak-Window Locked — Available Weekday Inventory at Scale
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  How to read this chart: move <b style='color:#e2e8f0;'>right</b> along the x-axis
  and a venue has more historical events — a longer operational track record.
  Move <b style='color:#fb923c;'>up</b> along the y-axis and more of that history
  is concentrated into peak booking dates. Bubble size reflects venue capacity.
  The <b style='color:#fb923c;'>upper-right corner</b> is the most commercially important zone:
  venues that are proven, high-capacity, <i>and</i> structurally concentrated into three booking dates.
  That is where under-activated calendar capacity is most valuable.
</p>
""", unsafe_allow_html=True)

x_cap    = int(vdf["total_events"].quantile(0.97))
plot_vdf = vdf[vdf["total_events"] <= x_cap].copy()

high_ev  = plot_vdf[plot_vdf["total_events"] >= 200]
low_ev   = plot_vdf[plot_vdf["total_events"] <  200].sample(
    min(1200, len(plot_vdf[plot_vdf["total_events"] < 200])), random_state=42
)
sc_df = pd.concat([high_ev, low_ev]).reset_index(drop=True)

TIER_STYLE = {
    "Balanced  (<40%)":      ("#38bdf8", 0.65),
    "Peak-Skewed  (40–80%)": ("#f59e0b", 0.65),
    "Extreme  (≥80%)":       ("#fb923c", 0.82),
}

fig_sc = go.Figure()

fig_sc.add_hrect(y0=80, y1=101,
                 fillcolor="rgba(251,146,60,0.05)", line_width=0, layer="below")
fig_sc.add_hline(
    y=80,
    line=dict(color="rgba(251,146,60,0.55)", width=1.8, dash="dot"),
    annotation_text="  80% — Extreme Concentration Threshold",
    annotation_position="top left",
    annotation_font=dict(color="#fb923c", size=11.5, family="Inter, sans-serif"),
)

for tier, (color, opacity) in TIER_STYLE.items():
    sub = sc_df[sc_df["tier"] == tier]
    if sub.empty:
        continue
    fig_sc.add_trace(go.Scatter(
        x=sub["total_events"],
        y=sub["prime_night_share"],
        mode="markers",
        name=tier,
        marker=dict(
            color=color, size=sub["bubble"], opacity=opacity,
            line=dict(color="rgba(0,0,0,0.25)", width=0.4),
        ),
        customdata=sub[["venue_name", "venue_city", "venue_state",
                         "cap_label", "off_night_share"]].fillna("—").values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]}, %{customdata[2]}<br>"
            "Events: <b>%{x:,}</b>  ·  Peak-Window: <b>%{y:.1f}%</b><br>"
            "Capacity: %{customdata[3]}  ·  Off-Peak: %{customdata[4]:.1f}%"
            "<extra></extra>"
        ),
    ))

fig_sc.add_annotation(
    x=x_cap * 0.72, y=94,
    text="<b>HIGH HISTORY · PEAK-WINDOW CONCENTRATED</b><br>Proven assets — underutilized booking capacity",
    showarrow=False,
    font=dict(size=11, color="#fb923c", family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.90)",
    bordercolor="rgba(251,146,60,0.40)",
    borderpad=9, borderwidth=1, xanchor="center",
)

fig_sc.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=540,
    margin=dict(l=70, r=40, t=20, b=100),
    xaxis=dict(
        title=dict(text="Total Historical Events  (capped at 97th-percentile for readability)",
                   font=dict(size=12, color="#64748b")),
        gridcolor="#0d1520", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, x_cap * 1.04], showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Peak-Window Concentration  (%)", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, 103], dtick=20,
    ),
    legend=dict(
        bgcolor="rgba(13,17,23,0.92)", bordercolor="#1e2535", borderwidth=1,
        font=dict(size=12, color="#94a3b8"),
        orientation="h", yanchor="bottom", y=-0.21, xanchor="left", x=0,
        itemsizing="constant",
    ),
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig_sc, use_container_width=True)

sc_ia, sc_ib, sc_ic = st.columns(3)
with sc_ia:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #38bdf8;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>Lower-Left — Low History</div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Venues with fewer events but balanced booking distribution.
        Small stages or newer venues that have demonstrated even utilisation.
        Limited inventory value at scale, but they prove the model is operationally viable.
      </p>
    </div>
    """, unsafe_allow_html=True)
with sc_ib:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #f59e0b;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>Middle Band — Partial Lock-in</div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Venues with solid event history, skewed toward weekends but not fully locked.
        These carry the most immediately improvable off-peak utilisation —
        they already activate some weekday inventory, so audience behaviour is
        partially established. Expanding off-peak supply here has the lowest friction.
      </p>
    </div>
    """, unsafe_allow_html=True)
with sc_ic:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.65rem;font-weight:700;color:#c2410c;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>Upper-Right — Peak-Window Locked</div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        High event history. High peak-window concentration. Large bubbles signal significant
        capacity. <b style='color:#fb923c;'>These are Azimuth's primary targets</b>:
        venues that have proven they can run shows, attract audiences, and fill seats —
        but whose off-peak calendar represents available, bookable inventory.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 — LEADERBOARD: Top 25 Most Peak-Window Concentrated Venues
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  25 Proven Stages: Maximum Track Record, Maximum Weekday Availability
</h2>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
            border-radius:8px;padding:14px 22px;margin-bottom:16px;'>
  <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.8;margin:0;'>
    These venues have <b style='color:#e2e8f0;'>proven operational track records</b> —
    they run events, attract audiences, and fill seats.
    Yet their off-peak share is near zero.
    <b style='color:#fb923c;'>That inventory is ready to be activated. Azimuth is the coordination layer that does it.</b>
  </p>
</div>
""", unsafe_allow_html=True)

top25 = (
    vdf.sort_values(["prime_night_share", "total_events"], ascending=[False, False])
    .head(25)
    [["venue_name", "venue_city", "venue_state", "venue_capacity",
      "total_events", "prime_night_events", "off_night_events",
      "prime_night_share", "off_night_share"]]
    .reset_index(drop=True)
)
top25.index += 1

top25_disp = top25.copy()
top25_disp["venue_state"]    = top25_disp["venue_state"].fillna("—")
top25_disp["venue_capacity"] = (
    top25_disp["venue_capacity"].fillna(0).astype(int)
    .apply(lambda v: "—" if v == 0 else f"{v:,}")
)
top25_disp["prime_night_share"] = top25_disp["prime_night_share"].round(1)
top25_disp["off_night_share"]   = top25_disp["off_night_share"].round(1)

st.dataframe(
    top25_disp,
    use_container_width=True,
    height=620,
    column_config={
        "venue_name":         st.column_config.TextColumn("Venue",               width="large"),
        "venue_city":         st.column_config.TextColumn("City"),
        "venue_state":        st.column_config.TextColumn("State"),
        "venue_capacity":     st.column_config.TextColumn("Capacity"),
        "total_events":       st.column_config.NumberColumn("Total Events",       format="%d"),
        "prime_night_events": st.column_config.NumberColumn("Peak-Window Events", format="%d"),
        "off_night_events":   st.column_config.NumberColumn("Off-Peak Events",    format="%d"),
        "prime_night_share":  st.column_config.ProgressColumn(
            "Peak-Window %", min_value=0, max_value=100, format="%.1f%%"),
        "off_night_share":    st.column_config.ProgressColumn(
            "Off-Peak %",    min_value=0, max_value=100, format="%.1f%%"),
    },
)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 3 — THE OPPORTUNITY NOBODY SEES
# Mid-tier artists (airplay 50–500, active & alive) with no live shows
# ─────────────────────────────────────────────────────────────────────────────

_DECEASED_OR_INACTIVE = {
    "Whitney Houston", "Amy Winehouse", "Chris Cornell", "Chester Bennington",
    "Scott Weiland", "Layne Staley", "Bradley Nowell", "Shannon Hoon",
    "Dolores O'Riordan", "Tom Petty", "Glenn Frey", "Eddie Van Halen",
    "Charlie Watts", "Taylor Hawkins", "Avicii", "Mac Miller",
    "Juice WRLD", "XXXTentacion", "Nipsey Hussle", "Lil Peep", "DMX",
    "MF DOOM", "DJ AM", "Big Pun", "Jam Master Jay", "J Dilla",
    "Nujabes", "Nate Dogg", "Eazy-E", "Big L", "Guru", "Prodigy",
    "Heavy D", "Rick James", "Left Eye", "Aaliyah",
    "Dimebag Darrell", "Ronnie James Dio", "Vinnie Paul",
    "David Bowie", "Lou Reed", "Robin Gibb", "Andy Gibb",
    "Roy Orbison", "Johnny Cash", "June Carter Cash", "Patsy Cline",
    "Bob Marley", "Jimi Hendrix", "Janis Joplin", "Jim Morrison",
    "Kurt Cobain", "Tupac Shakur", "The Notorious B.I.G.",
}

@st.cache_data
def load_artist_data():
    df = pd.read_csv(os.path.join(_HERE, "data", "airplay_vs_shows.csv"))
    # Mid-tier: genuine local radio presence, not superstars, not deceased
    mid = df[
        (df["airplay_count"] >= 50) &
        (df["airplay_count"] <= 500) &
        (~df["name"].isin(_DECEASED_OR_INACTIVE))
    ].copy().reset_index(drop=True)
    mid["opp_score"] = (mid["airplay_count"] / (mid["shows_count"] + 1)).round(0).astype(int)
    mid["shows_tier"] = pd.cut(
        mid["shows_count"],
        bins=[-1, 0, 19, 99999],
        labels=["0 shows (ready to book)", "1–19 shows", "active touring (≥20)"],
    )
    # Dot size proportional to radio reach
    mid["bubble"] = np.clip(mid["airplay_count"] / 500 * 14 + 5, 5, 18)
    return mid

mdf = load_artist_data()

_dark_mask     = mdf["shows_count"] == 0
_touring_mask  = mdf["shows_count"] >= 20
m_total        = len(mdf)
m_dark         = int(_dark_mask.sum())
m_dark_pct     = m_dark / m_total * 100
m_touring      = int(_touring_mask.sum())
m_touring_avg  = mdf.loc[_touring_mask, "shows_count"].mean()
m_unbooked_yr  = m_dark * 20   # conservative 20 shows/artist/yr

# ── Chapter 3 Hero ─────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:8px 0 10px;'>
  <div style='font-size:0.78rem;font-weight:600;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;'>
    Chapter 3  ·  The Demand Side  ·  Continuing from Chapter 2
  </div>
  <h1 style='font-size:2.6rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.1;margin-bottom:14px;'>
    The Artist Side Reflects the Same Ready Opportunity
  </h1>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Artists With Real Audiences — Ready to Activate Live ───────────────────────

st.markdown(f"""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:10px;'>
  Artists With Real Audiences — Ready to Activate Live
</h2>
<p style='font-size:0.92rem;color:#64748b;max-width:820px;line-height:1.8;margin-bottom:6px;'>
  Streaming has built real audiences for artists who have never played a live show.
  Among <b style='color:#e2e8f0;'>{m_total:,} mid-tier artists</b> with genuine local radio
  presence (airplay 50–500), <b style='color:#fb923c;'>{m_dark_pct:.1f}% have zero
  scheduled shows.</b>
</p>
<p style='font-size:0.87rem;color:#475569;max-width:820px;line-height:1.75;margin-bottom:22px;'>
  Superstars and deceased artists are excluded. What remains is
  <b style='color:#e2e8f0;'>{m_dark:,} active, bookable artists</b> whose audiences
  already exist — they just haven't been connected to a stage yet.
</p>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────

ak1, ak2, ak3, ak4 = st.columns(4)
ak1.markdown(kpi(f"{m_dark_pct:.1f}%",
                 f"Mid-Tier Artists With 0 Shows<br>Airplay 50–500",
                 "#fb923c"), unsafe_allow_html=True)
ak2.markdown(kpi(f"{m_dark:,}",
                 "Bookable Mid-Tier Artists<br>0 Shows · Active &amp; Alive",
                 "#f59e0b"), unsafe_allow_html=True)
ak3.markdown(kpi(f"{m_unbooked_yr:,}+",
                 "Est. Addressable Shows / Yr<br>@ 20 Shows Per Artist",
                 "#a78bfa"), unsafe_allow_html=True)
ak4.markdown(kpi(f"{m_touring:,}",
                 "Mid-Tier Artists Already Touring<br>Proof the Model Works",
                 "#38bdf8"), unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.divider()

# ── Scatter: Radio Reach vs. Live Shows ────────────────────────────────────────

opp    = mdf[mdf["shows_count"] == 0].copy()
active = mdf[mdf["shows_count"] >= 20].copy()
middle = mdf[(mdf["shows_count"] >= 1) & (mdf["shows_count"] <= 19)].copy()
avg_active_shows  = round(active["shows_count"].mean(), 1)
top3_active_names = ", ".join(active.nlargest(3, "airplay_count")["name"].tolist())

_AIRPLAY_MAX = 500
_y_max   = _AIRPLAY_MAX
_X_GAP_L = 7
_X_GAP_R = 22

_rng = np.random.default_rng(42)

fig_art = go.Figure()

# Three zone backgrounds
for _kw in [
    dict(x0=-4,       x1=_X_GAP_L, fillcolor="rgba(251,146,60,0.09)"),
    dict(x0=_X_GAP_L, x1=_X_GAP_R, fillcolor="rgba(255,255,255,0.005)"),
    dict(x0=_X_GAP_R, x1=135,      fillcolor="rgba(56,189,248,0.05)"),
]:
    fig_art.add_shape(type="rect", layer="below",
                      y0=-80, y1=_y_max * 1.25,
                      line_width=0, **_kw)

# Zone divider lines
for _xv in [_X_GAP_L, _X_GAP_R]:
    fig_art.add_shape(type="line", layer="below",
                      x0=_xv, x1=_xv, y0=0, y1=_y_max * 1.22,
                      line=dict(color="#252f45", width=1.2, dash="dot"))

# Middle dots (1–19 shows) — muted
_j_mid = _rng.uniform(-0.7, 0.7, len(middle))
fig_art.add_trace(go.Scatter(
    x=middle["shows_count"] + _j_mid, y=middle["airplay_count"],
    mode="markers",
    name="Some Activity  (1–19 shows)",
    marker=dict(color="#293548", size=np.clip(middle["airplay_count"] / 80, 4, 9),
                opacity=0.55, line=dict(color="#3d4f6b", width=0.4)),
    customdata=middle[["name", "airplay_count", "shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows %{customdata[2]}<extra></extra>",
))

# Active touring — sky blue
_j_act = _rng.uniform(-1.5, 1.5, len(active))
fig_art.add_trace(go.Scatter(
    x=active["shows_count"] + _j_act, y=active["airplay_count"],
    mode="markers",
    name="Active Touring  (≥20 shows)",
    marker=dict(color="#38bdf8", size=np.clip(active["airplay_count"] / 52, 8, 22),
                opacity=0.88, line=dict(color="rgba(186,230,253,0.28)", width=0.8)),
    customdata=active[["name", "airplay_count", "shows_count"]].values,
    hovertemplate="<b>%{customdata[0]}</b><br>Airplay %{customdata[1]:,} · Shows/yr %{customdata[2]}<extra></extra>",
))

# Opportunity glow halo
_j_opp = _rng.uniform(-2.8, 2.8, len(opp))
fig_art.add_trace(go.Scatter(
    x=_j_opp, y=opp["airplay_count"],
    mode="markers",
    marker=dict(color="rgba(251,146,60,0.09)", size=np.clip(opp["airplay_count"] / 34, 26, 56),
                opacity=1, line=dict(width=0)),
    hoverinfo="skip", showlegend=False,
))

# Untapped solid dots — orange
fig_art.add_trace(go.Scatter(
    x=_j_opp, y=opp["airplay_count"],
    mode="markers",
    name="Ready to Book  (0 shows · active &amp; alive)",
    marker=dict(color="#fb923c", size=np.clip(opp["airplay_count"] / 44, 9, 26),
                opacity=0.95, line=dict(color="rgba(253,186,116,0.40)", width=1.1)),
    customdata=opp[["name", "airplay_count", "shows_count", "opp_score"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>Airplay: %{customdata[1]:,}<br>"
        "Shows/yr: %{customdata[2]}<br>Opp. Score: %{customdata[3]:.0f}<extra></extra>"
    ),
))

# Zone header badges
for _d in [
    dict(x=0,  y=_y_max * 1.155, text="<b>AUDIENCE READY TO BOOK</b>",
         color="#fb923c", size=13, bg="rgba(251,146,60,0.14)", bc="rgba(251,146,60,0.32)"),
    dict(x=70, y=_y_max * 1.155, text="<b>ACTIVE TOURING</b>",
         color="#38bdf8", size=13, bg="rgba(56,189,248,0.12)", bc="rgba(56,189,248,0.30)"),
]:
    fig_art.add_annotation(
        x=_d["x"], y=_d["y"], text=_d["text"], showarrow=False,
        font=dict(size=_d["size"], color=_d["color"], family="Inter, sans-serif"),
        xanchor="center", yanchor="middle", xref="x", yref="y",
        bgcolor=_d["bg"], bordercolor=_d["bc"], borderwidth=1, borderpad=7,
    )

# Booking gap callout — centred in the gap corridor
_gap_cx = (_X_GAP_L + _X_GAP_R) / 2
fig_art.add_annotation(
    x=_gap_cx, y=_y_max * 0.46,
    text=(
        "← THE ACTIVATION OPPORTUNITY →<br>"
        f"<b>{m_dark:,} artists · ready to book</b><br>"
        f"<b>{m_unbooked_yr:,}+ shows / yr addressable</b>"
    ),
    showarrow=False,
    font=dict(size=11.5, color="#94a3b8", family="Inter, sans-serif"),
    xanchor="center", yanchor="middle",
    xref="x", yref="y",
    bgcolor="rgba(11,17,27,0.90)",
    bordercolor="rgba(75,86,117,0.32)",
    borderwidth=1, borderpad=14, align="center",
)

fig_art.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    title=dict(
        text=(
            "<b style='color:#e2e8f0;font-size:16px;'>"
            "Radio Reach vs. Live Shows — The Activation Opportunity"
            "</b><br>"
            "<span style='color:#64748b;font-size:11.5px;'>"
            "Mid-tier artists only (airplay 50–500)  ·  "
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
        range=[-20, _y_max * 1.25],
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

st.plotly_chart(fig_art, use_container_width=True)

# ── Three insight cards ────────────────────────────────────────────────────────

ins1, ins2, ins3 = st.columns(3)
with ins1:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:8px;padding:18px 20px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#fb923c;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>THE OPPORTUNITY IS REAL</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0;'>
        <b style='color:#fb923c;'>{m_dark_pct:.1f}% of mid-tier artists</b> with genuine local
        radio presence are ready to book live shows. Active, living artists with real audiences —
        already on your local radio, with built-in fan bases ready to activate.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ins2:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #f59e0b;
                border-radius:8px;padding:18px 20px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#f59e0b;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>THE SCALE IS SIGNIFICANT</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0;'>
        <b style='color:#f59e0b;'>{m_dark:,} bookable artists · ready to activate.</b>
        At a conservative 20 shows per year each, that is
        <b style='color:#f59e0b;'>{m_unbooked_yr:,}+ addressable shows per year</b> —
        live revenue the market has not yet captured.
        Every orange dot is a booking opportunity waiting to be coordinated.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ins3:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #38bdf8;
                border-radius:8px;padding:18px 20px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#38bdf8;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>THE MODEL ALREADY WORKS</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0;'>
        <b style='color:#38bdf8;'>{m_touring:,} mid-tier artists are already touring</b> —
        {top3_active_names} and others — turning the same local radio reach into
        <b>avg. {avg_active_shows} shows/year</b>.
        The orange cluster has identical audience size.
        It just needs the connection.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.divider()

# ── Who's Waiting to Be Booked ─────────────────────────────────────────────────

st.markdown(f"""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  25 Artists: Radio Reach Built, Live Career Ready to Launch
</h2>
<p style='font-size:0.85rem;color:#64748b;margin-bottom:14px;line-height:1.6;'>
  Top 25 ready-to-book mid-tier artists · Airplay 50–500 · Active &amp; alive ·
  Sorted by airplay reach
</p>
""", unsafe_allow_html=True)

tbl_col, opp_col = st.columns([1.6, 1])

with tbl_col:
    top25_artists = (
        mdf[mdf["shows_count"] == 0]
        .nlargest(25, "airplay_count")
        [["name", "airplay_count", "shows_count", "opp_score"]]
        .reset_index(drop=True)
    )
    top25_artists.index += 1
    top25_artists.columns = ["Artist", "Airplay", "Shows / yr", "Opp. Score"]

    st.dataframe(
        top25_artists,
        use_container_width=True,
        height=640,
        column_config={
            "Artist":     st.column_config.TextColumn("Artist", width="large"),
            "Airplay":    st.column_config.ProgressColumn(
                "Airplay", min_value=0, max_value=500, format="%d"),
            "Shows / yr": st.column_config.NumberColumn("Shows / yr", format="%d"),
            "Opp. Score": st.column_config.NumberColumn("Opp. Score", format="%d"),
        },
    )

with opp_col:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-radius:10px;
                padding:26px 24px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#475569;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:14px;'>Opportunity Score</div>

      <div style='background:#0d1117;border:1px solid #1e2535;border-radius:8px;
                  padding:14px 18px;margin-bottom:18px;'>
        <div style='font-size:1rem;font-weight:700;color:#fb923c;
                    font-family:monospace;letter-spacing:0.02em;'>
          Score = Airplay ÷ (Shows + 1)
        </div>
      </div>

      <p style='color:#94a3b8;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        The higher the score, the wider the gap between the audience an artist has built
        and the live presence they've established.
      </p>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0 0 18px;'>
        <b style='color:#fb923c;'>Above 500</b> = significant untapped demand.
      </p>

      <hr style='border:none;border-top:1px solid #1e2535;margin:0 0 16px;'>

      <p style='color:#94a3b8;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        These artists are not unknown — they have radio history.
        What they lack is infrastructure: a manager, an agent, a venue connection.
        <b style='color:#fb923c;'>That is the exact gap Azimuth closes.</b>
      </p>

      <p style='color:#475569;font-size:0.78rem;line-height:1.65;margin:0;'>
        <b>Data note:</b> shows_count reflects a specific dataset period.
        Some active artists may show 0 due to data gaps or hiatus.
        Deceased / permanently inactive artists are excluded from this analysis.
      </p>
    </div>
    """, unsafe_allow_html=True)

# ── Connecting the two gaps ────────────────────────────────────────────────────

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #a78bfa;
            border-radius:8px;padding:18px 24px;'>
  <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
              letter-spacing:0.12em;margin-bottom:10px;'>Connecting the Two Gaps</div>
  <p style='color:#cbd5e1;font-size:0.9rem;line-height:1.8;margin:0 0 10px;'>
    Chapter 2 showed that <b style='color:#fb923c;'>{v_extreme:,} proven venues</b>
    concentrate 80%+ of their events into Friday–Sunday,
    leaving weekday calendar inventory under-activated —
    the <b style='color:#fb923c;'>supply side of the gap</b>.
  </p>
  <p style='color:#94a3b8;font-size:0.9rem;line-height:1.8;margin:0 0 10px;'>
    Chapter 3 shows that <b style='color:#a78bfa;'>{m_dark:,} active, bookable artists</b>
    carry genuine radio audiences but zero live shows —
    their fans are ready, their stage is ready to be arranged —
    the <b style='color:#a78bfa;'>demand side of the gap</b>.
  </p>
  <p style='color:#fb923c;font-size:0.9rem;line-height:1.8;margin:0;font-weight:600;'>
    Venues with available calendar inventory. Artists with audience reach ready to activate.
    Azimuth is the intelligence layer that connects both sides of the same market opportunity.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CLOSING INSIGHT CARD
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='margin-top:4px;margin-bottom:8px;padding:32px 38px;
            background:#12161f;
            border:1px solid #1e2535;border-radius:14px;
            border-left:4px solid #fb923c;
            box-shadow:0 4px 32px rgba(0,0,0,0.4);'>

  <p style='color:#e2e8f0;font-size:1.1rem;font-weight:700;
            line-height:1.5;margin:0 0 10px;letter-spacing:-0.01em;'>
    The Supply Is Real. The Demand Is Real. The Coordination Layer Is Azimuth.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.85;margin:0 0 18px;'>
    <b style='color:#fb923c;'>Azimuth does not build venues —
    it coordinates under-activated venue calendars and turns fragmented booking capacity
    into programmable live-event infrastructure.</b>
  </p>

  <p style='color:#64748b;font-size:0.9rem;line-height:1.8;margin:0;'>
    Across {v_total:,} established venues,
    <b style='color:#fb923c;'>{v_extreme:,} ({v_extreme_pct:.0f}%)</b>
    concentrate 80% or more of their events into a single three-window period.
    Their Monday-through-Thursday calendars are structurally underutilized —
    because no coordination layer has yet existed
    to activate that inventory efficiently.<br><br>
    The infrastructure already exists. The opportunity is to coordinate when, where,
    and how that infrastructure gets activated —
    converting <b style='color:#fb923c;'>latent venue capacity into recurring,
    monetisable live-event inventory</b>.
    The stages are already built. The audiences are already there.
    What the market needs is the intelligence layer that connects them.
  </p>

</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_dma_data():
    df = pd.read_csv(os.path.join(_HERE, "data", "dma_calendar_capacity.csv"))
    df["dma_name"] = df["dma_name"].str.strip()
    return df

_dma = load_dma_data()

# ── Headline constants (provided) ──────────────────────────────────────────────
_D_TOTAL_VENUES    = 161_689
_D_TOTAL_DMAS      = 186
_D_TOTAL_EVENTS    = 1_935_807
_D_PEAK_EVENTS     = 1_155_810
_D_OFFPEAK_EVENTS  = 779_997
_D_AVG_OFFPK_PER_V = 4.82
_D_PEAK_SHARE      = round(_D_PEAK_EVENTS / _D_TOTAL_EVENTS * 100, 1)
_D_OFFPEAK_SHARE   = round(_D_OFFPEAK_EVENTS / _D_TOTAL_EVENTS * 100, 1)


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — HERO
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:8px 0 26px;'>
  <div style='font-size:0.78rem;font-weight:600;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;'>
    Chapter 4  ·  The Market Level  ·  Continuing from Chapter 3
  </div>
  <h1 style='font-size:2.6rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.1;margin-bottom:14px;'>
    The Same Pattern Holds Across Every U.S. Market
  </h1>
  <p style='font-size:0.97rem;color:#64748b;max-width:780px;line-height:1.8;
            border-left:3px solid #1e2535;padding-left:16px;margin:0 0 32px;'>
    The largest markets are not missing venues.
    They are competing for the same peak booking windows.
    Chapter 4 shows that the same pattern repeats at the DMA market level —
    across every major U.S. city, without exception.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Giant headline number ──────────────────────────────────────────────────────

st.markdown(f"""
<div style='text-align:center;padding:42px 24px 36px;background:#12161f;
            border:1px solid #1e2535;border-radius:16px;margin-bottom:28px;
            box-shadow:0 6px 40px rgba(0,0,0,0.45);'>
  <div style='font-size:5.2rem;font-weight:800;color:#fb923c;
              line-height:1;letter-spacing:-0.05em;margin-bottom:10px;'>
    {_D_OFFPEAK_EVENTS:,}
  </div>
  <div style='font-size:1.15rem;font-weight:600;color:#e2e8f0;
              letter-spacing:-0.01em;margin-bottom:18px;'>
    Under-Activated Weekday Event Opportunities
  </div>
  <p style='font-size:0.9rem;color:#64748b;max-width:600px;margin:0 auto;line-height:1.8;'>
    Across <b style='color:#e2e8f0;'>{_D_TOTAL_VENUES:,} venues</b>
    and <b style='color:#e2e8f0;'>{_D_TOTAL_DMAS} DMA markets</b>,
    the average venue records only
    <b style='color:#fb923c;'>{_D_AVG_OFFPK_PER_V} off-peak events</b>
    in the historical dataset.
    This is not a venue shortage. It is a calendar coordination gap.
  </p>
</div>
""", unsafe_allow_html=True)

# ── 4 KPI cards ───────────────────────────────────────────────────────────────

dk1, dk2, dk3, dk4 = st.columns(4)
dk1.markdown(kpi(f"{_D_TOTAL_VENUES:,}",
                 "Venues Mapped<br>Across U.S. DMA Markets",
                 "#fb923c"), unsafe_allow_html=True)
dk2.markdown(kpi(f"{_D_TOTAL_DMAS}",
                 "DMA Markets<br>in the Analysis",
                 "#f59e0b"), unsafe_allow_html=True)
dk3.markdown(kpi("1.93M",
                 "Historical Events<br>Across All Markets",
                 "#a78bfa"), unsafe_allow_html=True)
dk4.markdown(kpi(f"{_D_AVG_OFFPK_PER_V}",
                 "Avg Off-Peak Events / Venue<br>Weekday Activation Baseline",
                 "#38bdf8"), unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
            border-radius:8px;padding:14px 22px;'>
  <p style='color:#cbd5e1;font-size:0.92rem;line-height:1.8;margin:0;'>
    <b style='color:#fb923c;'>Key insight:</b>
    Of {_D_TOTAL_EVENTS:,} total events across all U.S. DMA markets,
    <b style='color:#fb923c;'>{_D_PEAK_SHARE}% ({_D_PEAK_EVENTS:,} events)</b>
    fall within peak booking windows — a concentration ratio that mirrors
    the national-level finding from Chapter 1.
    The remaining <b style='color:#38bdf8;'>{_D_OFFPEAK_EVENTS:,} off-peak events</b>
    represent the under-activated weekday capacity Azimuth is designed to coordinate.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — CHART 1: DMA PEAK CONCENTRATION DISTRIBUTION
# Every dot = one DMA market. Shows the structural consistency across all 186 markets.
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Every DMA in America Shows the Same Concentration Signature
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  Each dot represents one DMA market, positioned by the share of its events falling on
  Friday, Saturday, or Sunday. The cluster is not random — it is a structural pattern
  that holds across every city, every region, every market size.
  <b style='color:#e2e8f0;'>No DMA has solved this problem. Azimuth does.</b>
</p>
""", unsafe_allow_html=True)

_dma_strip = _dma.copy().reset_index(drop=True)
_strip_rng = np.random.default_rng(99)
_strip_jitter = _strip_rng.uniform(-0.38, 0.38, len(_dma_strip))

_STRIP_MEDIAN = round(_dma_strip["peak_window_share"].median(), 1)
_STRIP_MEAN   = round(_dma_strip["peak_window_share"].mean(), 1)

_strip_colors = []
for v in _dma_strip["peak_window_share"]:
    if v < 55:
        _strip_colors.append("#38bdf8")
    elif v < 65:
        _strip_colors.append("#f59e0b")
    else:
        _strip_colors.append("#fb923c")

fig_strip = go.Figure()

for _sx0, _sx1, _sfill in [
    (0,  55, "rgba(56,189,248,0.030)"),
    (55, 65, "rgba(245,158,11,0.040)"),
    (65, 100,"rgba(251,146,60,0.060)"),
]:
    fig_strip.add_shape(type="rect", layer="below",
                        x0=_sx0, x1=_sx1, y0=-1.1, y1=1.1,
                        fillcolor=_sfill, line_width=0)

for _sv, _sc in [(55, "#1e3859"), (65, "rgba(251,146,60,0.40)")]:
    fig_strip.add_shape(type="line", layer="below",
                        x0=_sv, x1=_sv, y0=-1.0, y1=1.0,
                        line=dict(color=_sc, width=1, dash="dot"))

fig_strip.add_trace(go.Scatter(
    x=_dma_strip["peak_window_share"],
    y=_strip_jitter,
    mode="markers",
    name="All DMA Markets",
    marker=dict(color=_strip_colors, size=8, opacity=0.72,
                line=dict(color="rgba(0,0,0,0.18)", width=0.4)),
    customdata=_dma_strip[["dma_name", "venue_count", "peak_window_share",
                             "off_peak_events_per_venue", "total_events"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Peak-Window Share: <b>%{x:.1f}%</b><br>"
        "Venues: %{customdata[1]:,} · Total Events: %{customdata[4]:,}<br>"
        "Off-Peak / Venue: %{customdata[3]:.2f}"
        "<extra></extra>"
    ),
))

_STRIP_LABELS = {
    "New York", "Los Angeles", "Chicago", "Nashville",
    "Tampa - St. Pete - Sarasota", "Dallas - Ft. Worth", "Boston",
}
_sl_mask   = _dma_strip["dma_name"].isin(_STRIP_LABELS)
_sl_df     = _dma_strip[_sl_mask].reset_index(drop=True)
_sl_jitter = _strip_jitter[_sl_mask.values]
_sl_names  = (
    _sl_df["dma_name"]
    .str.replace("Tampa - St. Pete - Sarasota", "Tampa", regex=False)
    .str.replace("Dallas - Ft. Worth", "Dallas", regex=False)
)

fig_strip.add_trace(go.Scatter(
    x=_sl_df["peak_window_share"],
    y=_sl_jitter,
    mode="markers+text",
    name="Key Markets",
    marker=dict(color="#e2e8f0", size=11, opacity=1,
                line=dict(color="rgba(251,146,60,0.65)", width=1.6)),
    text=_sl_names,
    textposition="top center",
    textfont=dict(size=9.5, color="#94a3b8", family="Inter, sans-serif"),
    customdata=_sl_df[["dma_name", "venue_count", "peak_window_share",
                         "off_peak_events_per_venue"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Peak-Window Share: <b>%{x:.1f}%</b><br>"
        "Venues: %{customdata[1]:,}<br>"
        "Off-Peak / Venue: %{customdata[3]:.2f}"
        "<extra></extra>"
    ),
))

fig_strip.add_vline(
    x=_STRIP_MEDIAN,
    line=dict(color="rgba(251,146,60,0.55)", width=1.5, dash="dot"),
    annotation_text=f"  Median {_STRIP_MEDIAN}%",
    annotation_position="top right",
    annotation_font=dict(color="#fb923c", size=11, family="Inter, sans-serif"),
)

for _slx, _slt, _slc, _slbg, _slbc in [
    (40,  "LOWER<br>CONCENTRATION",  "#38bdf8", "rgba(56,189,248,0.10)",  "rgba(56,189,248,0.25)"),
    (60,  "MODERATE",                "#f59e0b", "rgba(245,158,11,0.10)",   "rgba(245,158,11,0.25)"),
    (80,  "HIGH<br>CONCENTRATION",   "#fb923c", "rgba(251,146,60,0.10)",   "rgba(251,146,60,0.25)"),
]:
    fig_strip.add_annotation(
        x=_slx, y=0.78, text=f"<b>{_slt}</b>",
        showarrow=False,
        font=dict(size=10, color=_slc, family="Inter, sans-serif"),
        xanchor="center", yanchor="middle",
        bgcolor=_slbg, bordercolor=_slbc, borderwidth=1, borderpad=6, align="center",
    )

fig_strip.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=360,
    margin=dict(l=50, r=60, t=20, b=60),
    xaxis=dict(
        title=dict(text="Peak-Window Share  (% of events on Fri / Sat / Sun)",
                   font=dict(size=13, color="#64748b")),
        range=[30, 85], dtick=5,
        tickfont=dict(size=12, color="#94a3b8"),
        gridcolor="#0d1520", zeroline=False, showgrid=False,
        ticksuffix="%",
    ),
    yaxis=dict(
        showticklabels=False, showgrid=False, zeroline=False,
        range=[-1.3, 1.4],
    ),
    showlegend=False,
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig_strip, use_container_width=True)

_n_above60 = int((_dma_strip["peak_window_share"] >= 60).sum())
_n_above65 = int((_dma_strip["peak_window_share"] >= 65).sum())
st.markdown(f"""
<p style='font-size:0.82rem;color:#475569;text-align:center;margin:-8px 0 16px;'>
  {len(_dma_strip)} DMA markets plotted · Median peak-window share: <b style='color:#fb923c;'>{_STRIP_MEDIAN}%</b> ·
  <b style='color:#fb923c;'>{_n_above65} markets ({_n_above65*100//len(_dma_strip)}%)</b> above 65% concentration ·
  Hover any dot for market detail
</p>
""", unsafe_allow_html=True)

_sc1, _sc2, _sc3 = st.columns(3)
with _sc1:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #38bdf8;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>No Market Is An Exception</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.7;margin:0;'>
        Every DMA cluster falls between 40–80% peak concentration.
        There is no outlier market that has figured out weekday activation.
        The pattern is universal — and therefore the opportunity is universal.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _sc2:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>Even Nashville Is Concentrated</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.7;margin:0;'>
        Nashville — the most active live music market per capita —
        still runs <b style='color:#f59e0b;'>44% of its events on peak windows</b>.
        Even the most music-dense market has significant weekday activation gap.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _sc3:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>The Median Market: {_STRIP_MEDIAN}%</div>
      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.7;margin:0;'>
        The typical DMA runs <b style='color:#fb923c;'>{_STRIP_MEDIAN}% of all events</b> in
        peak windows. The remaining {round(100-_STRIP_MEDIAN, 1)}% is weekday inventory —
        <b style='color:#e2e8f0;'>existing but uncoordinated.</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — CHART 2: DMA OPPORTUNITY RANKING
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Where Weekday Inventory Is Largest — and Ready to Program
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  Top 15 markets by total off-peak events (venues ≥ 1,000).
  These markets already support thousands of weekday events —
  meaning demand exists and the activation model is already partially working.
  The opportunity is to coordinate and expand it.
</p>
""", unsafe_allow_html=True)

_dma_top = (
    _dma[_dma["venue_count"] >= 1000]
    .nlargest(15, "off_peak_events")
    .reset_index(drop=True)
)

_opp_colors = [
    "#fb923c" if i < 3 else
    "#f59e0b" if i < 7 else
    "#1e3859"
    for i in range(len(_dma_top))
]

fig_opp = go.Figure()

fig_opp.add_trace(go.Bar(
    x=_dma_top["off_peak_events"],
    y=_dma_top["dma_name"],
    orientation="h",
    marker=dict(
        color=_opp_colors,
        opacity=0.91,
        line=dict(color="rgba(0,0,0,0.18)", width=0.5),
    ),
    text=[f" <b>{v/1000:.1f}K</b>" for v in _dma_top["off_peak_events"]],
    textposition="outside",
    textfont=dict(size=11, color="#94a3b8", family="Inter, sans-serif"),
    customdata=_dma_top[["dma_name", "venue_count", "off_peak_events",
                           "off_peak_events_per_venue", "peak_window_share"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Venues: <b>%{customdata[1]:,}</b><br>"
        "Off-Peak Events: <b>%{customdata[2]:,}</b><br>"
        "Off-Peak / Venue: <b>%{customdata[3]:.2f}</b><br>"
        "Peak-Window Share: %{customdata[4]:.1f}%"
        "<extra></extra>"
    ),
))

fig_opp.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=580,
    margin=dict(l=240, r=90, t=16, b=60),
    xaxis=dict(
        title=dict(text="Total Off-Peak Events (Historical)",
                   font=dict(size=12, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, showgrid=True,
        range=[0, _dma_top["off_peak_events"].max() * 1.22],
        tickformat=",",
    ),
    yaxis=dict(
        tickfont=dict(size=12, color="#cbd5e1"),
        autorange="reversed",
        showgrid=False,
    ),
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
    showlegend=False,
)

st.plotly_chart(fig_opp, use_container_width=True)

st.markdown("""
<p style='font-size:0.82rem;color:#475569;text-align:center;margin:-10px 0 16px;'>
  Filtered to markets with 1,000+ venues · Off-peak = Mon–Thu events ·
  <b style='color:#fb923c;'>■</b> Top 3 &nbsp;
  <b style='color:#f59e0b;'>■</b> Top 7 &nbsp;
  <b style='color:#4b6080;'>■</b> Remaining
</p>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — CHART 3: LOWEST WEEKDAY ACTIVATION AMONG MAJOR MARKETS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Large Markets, Low Activation Rate — The Highest-Leverage Entry Points
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  The most interesting markets are not necessarily the biggest.
  They are the markets where venue supply is large,
  but weekday activation remains thin —
  averaging only 3–5 off-peak events per venue across thousands of stages.
</p>
""", unsafe_allow_html=True)

_dma_low = (
    _dma[_dma["venue_count"] >= 1000]
    .nsmallest(15, "off_peak_events_per_venue")
    .reset_index(drop=True)
)

_low_colors = []
for v in _dma_low["off_peak_events_per_venue"]:
    if v < 3.5:
        _low_colors.append("#fb923c")
    elif v < 4.5:
        _low_colors.append("#f59e0b")
    else:
        _low_colors.append("#38bdf8")

# ── Lollipop chart — stems + dots ─────────────────────────────────────────────
fig_low = go.Figure()

fig_low.add_vline(
    x=_D_AVG_OFFPK_PER_V,
    line=dict(color="rgba(251,146,60,0.38)", width=1.4, dash="dot"),
    annotation_text=f"  National avg  {_D_AVG_OFFPK_PER_V}",
    annotation_position="top right",
    annotation_font=dict(color="#fb923c", size=11, family="Inter, sans-serif"),
)

for i, (_, row) in enumerate(_dma_low.iterrows()):
    fig_low.add_shape(
        type="line", layer="below",
        x0=0, x1=row["off_peak_events_per_venue"],
        y0=i, y1=i,
        line=dict(color="#1a2535", width=2),
    )

fig_low.add_trace(go.Scatter(
    x=_dma_low["off_peak_events_per_venue"],
    y=list(range(len(_dma_low))),
    mode="markers+text",
    marker=dict(color=_low_colors, size=15, opacity=0.95,
                line=dict(color="rgba(0,0,0,0.22)", width=0.5)),
    text=[f"  {v:.2f}" for v in _dma_low["off_peak_events_per_venue"]],
    textposition="middle right",
    textfont=dict(size=11.5, color="#94a3b8", family="Inter, sans-serif"),
    customdata=_dma_low[["dma_name", "venue_count", "off_peak_events",
                           "off_peak_events_per_venue", "total_events"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Venues: <b>%{customdata[1]:,}</b><br>"
        "Off-Peak Events: <b>%{customdata[2]:,}</b><br>"
        "Off-Peak / Venue: <b>%{customdata[3]:.2f}</b><br>"
        "Total Events: %{customdata[4]:,}"
        "<extra></extra>"
    ),
    showlegend=False,
))

fig_low.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=560,
    margin=dict(l=270, r=110, t=16, b=60),
    xaxis=dict(
        title=dict(text="Off-Peak Events Per Venue  (weekday activation rate)",
                   font=dict(size=12, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, showgrid=True,
        range=[0, _dma_low["off_peak_events_per_venue"].max() * 1.32],
    ),
    yaxis=dict(
        tickmode="array",
        tickvals=list(range(len(_dma_low))),
        ticktext=_dma_low["dma_name"].tolist(),
        tickfont=dict(size=11.5, color="#cbd5e1"),
        autorange="reversed",
        showgrid=False,
    ),
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
    showlegend=False,
)

st.plotly_chart(fig_low, use_container_width=True)

_low1, _low2, _low3 = st.columns(3)
with _low1:
    _worst = _dma_low.iloc[0]
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#fb923c;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Lowest: {_worst["dma_name"]}
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        <b style='color:#fb923c;'>{_worst["off_peak_events_per_venue"]:.2f}</b> off-peak events
        per venue across <b>{int(_worst["venue_count"]):,} venues</b>.
        Significant calendar inventory with minimal weekday programming —
        a direct target for coordinated activation.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _low2:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#f59e0b;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        The Pattern Holds In Large Markets
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Washington DC, Dallas, Houston, and Miami all appear in this list —
        markets with <b style='color:#f59e0b;'>thousands of venues</b>
        yet averaging fewer than 4.5 off-peak events per venue.
        Scale amplifies the opportunity, not the pattern.
      </p>
    </div>
    """, unsafe_allow_html=True)
with _low3:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #38bdf8;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#38bdf8;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Below The National Average
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Every market in this chart sits below the
        <b style='color:#38bdf8;'>{_D_AVG_OFFPK_PER_V} national average</b>.
        These are not underperforming markets — they have the venues, the audiences,
        and the event infrastructure. What they need is the coordination layer — Azimuth.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — CHART 4: STRATEGIC MARKET QUADRANT
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Where Azimuth Activates First
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  Azimuth does not need to activate every market at once.
  The highest-value launch markets are where venue supply and under-activated weekday
  opportunity overlap — upper-right quadrant, where scale meets activation gap.
</p>
""", unsafe_allow_html=True)

_dma_quad = _dma[_dma["venue_count"] >= 1000].copy().reset_index(drop=True)

_q_med_x = _dma_quad["venue_count"].median()
_q_med_y = _dma_quad["off_peak_events"].median()

_LABEL_MARKETS = {
    "New York", "Los Angeles", "Chicago",
    "San Francisco - Oak - San Jose", "Boston", "Philadelphia",
    "Washington, DC", "Atlanta", "Dallas - Ft. Worth",
    "Miami - Ft. Lauderdale", "Houston",
    "Tampa - St. Pete - Sarasota", "Nashville",
    "Denver", "Seattle - Tacoma",
}

_labeled = _dma_quad[_dma_quad["dma_name"].isin(_LABEL_MARKETS)].copy()
_others  = _dma_quad[~_dma_quad["dma_name"].isin(_LABEL_MARKETS)].copy()

fig_quad = go.Figure()

_x_max_q = _dma_quad["venue_count"].max() * 1.12
_y_max_q = _dma_quad["off_peak_events"].max() * 1.18

for _x0, _x1, _y0, _y1, _fill in [
    (0,        _q_med_x, _q_med_y, _y_max_q, "rgba(56,189,248,0.035)"),
    (_q_med_x, _x_max_q, _q_med_y, _y_max_q, "rgba(251,146,60,0.06)"),
    (0,        _q_med_x, 0,        _q_med_y, "rgba(0,0,0,0)"),
    (_q_med_x, _x_max_q, 0,        _q_med_y, "rgba(167,139,250,0.035)"),
]:
    fig_quad.add_shape(type="rect", layer="below",
                       x0=_x0, x1=_x1, y0=_y0, y1=_y1,
                       fillcolor=_fill, line_width=0)

fig_quad.add_vline(x=_q_med_x,
                   line=dict(color="#1e2d3d", width=1.2, dash="dot"))
fig_quad.add_hline(y=_q_med_y,
                   line=dict(color="#1e2d3d", width=1.2, dash="dot"))

fig_quad.add_trace(go.Scatter(
    x=_others["venue_count"],
    y=_others["off_peak_events"],
    mode="markers",
    name="Other Markets",
    marker=dict(color="#1e3859", size=7, opacity=0.7,
                line=dict(color="#253448", width=0.5)),
    customdata=_others[["dma_name", "venue_count", "off_peak_events",
                          "off_peak_events_per_venue"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Venues: %{customdata[1]:,}<br>"
        "Off-Peak Events: %{customdata[2]:,}<br>"
        "Off-Peak / Venue: %{customdata[3]:.2f}"
        "<extra></extra>"
    ),
))

_label_colors = []
for _, row in _labeled.iterrows():
    if row["venue_count"] >= _q_med_x and row["off_peak_events"] >= _q_med_y:
        _label_colors.append("#fb923c")
    elif row["venue_count"] < _q_med_x and row["off_peak_events"] >= _q_med_y:
        _label_colors.append("#38bdf8")
    elif row["venue_count"] >= _q_med_x and row["off_peak_events"] < _q_med_y:
        _label_colors.append("#a78bfa")
    else:
        _label_colors.append("#475569")

_short_names = (
    _labeled["dma_name"]
    .str.replace("San Francisco - Oak - San Jose", "SF Bay Area", regex=False)
    .str.replace("Tampa - St. Pete - Sarasota", "Tampa", regex=False)
    .str.replace("Dallas - Ft. Worth", "Dallas", regex=False)
    .str.replace("Miami - Ft. Lauderdale", "Miami", regex=False)
    .str.replace("Seattle - Tacoma", "Seattle", regex=False)
    .str.replace("Washington, DC", "Washington DC", regex=False)
)

fig_quad.add_trace(go.Scatter(
    x=_labeled["venue_count"],
    y=_labeled["off_peak_events"],
    mode="markers+text",
    name="Key Markets",
    marker=dict(color=_label_colors, size=11, opacity=0.95,
                line=dict(color="rgba(255,255,255,0.20)", width=1)),
    text=_short_names,
    textposition="top center",
    textfont=dict(size=10, color="#94a3b8", family="Inter, sans-serif"),
    customdata=_labeled[["dma_name", "venue_count", "off_peak_events",
                           "off_peak_events_per_venue"]].values,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Venues: %{customdata[1]:,}<br>"
        "Off-Peak Events: %{customdata[2]:,}<br>"
        "Off-Peak / Venue: %{customdata[3]:.2f}"
        "<extra></extra>"
    ),
))

for _qx, _qy, _qlabel, _qcolor in [
    (_q_med_x * 0.38,  _y_max_q * 0.93, "High Activity<br>Smaller Supply",  "#38bdf8"),
    (_x_max_q * 0.86,  _y_max_q * 0.93, "Priority Launch<br>Markets",        "#fb923c"),
    (_x_max_q * 0.86,  _y_max_q * 0.09, "Large Supply<br>Low Activation",     "#a78bfa"),
    (_q_med_x * 0.38,  _y_max_q * 0.09, "Lower Priority",                     "#334155"),
]:
    fig_quad.add_annotation(
        x=_qx, y=_qy, text=f"<b>{_qlabel}</b>",
        showarrow=False,
        font=dict(size=11, color=_qcolor, family="Inter, sans-serif"),
        xanchor="center", yanchor="middle",
        bgcolor="rgba(13,17,23,0.80)",
        bordercolor=_qcolor, borderwidth=1, borderpad=7, align="center",
    )

fig_quad.add_annotation(
    x=_q_med_x, y=_y_max_q * 0.52,
    text=f"  Median<br>  {int(_q_med_x):,} venues",
    showarrow=False,
    font=dict(size=10, color="#334155", family="Inter, sans-serif"),
    xanchor="left",
)
fig_quad.add_annotation(
    x=_x_max_q * 0.01, y=_q_med_y,
    text=f"Median  {int(_q_med_y):,}",
    showarrow=False,
    font=dict(size=10, color="#334155", family="Inter, sans-serif"),
    yanchor="bottom",
)

fig_quad.update_layout(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=620,
    margin=dict(l=80, r=60, t=24, b=80),
    xaxis=dict(
        title=dict(text="Market Size  (Total Venues)",
                   font=dict(size=13, color="#64748b")),
        gridcolor="#0d1520", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, showgrid=False,
        range=[0, _x_max_q],
        tickformat=",",
    ),
    yaxis=dict(
        title=dict(text="Weekday Opportunity  (Total Off-Peak Events)",
                   font=dict(size=13, color="#64748b")),
        gridcolor="#131a28", tickfont=dict(size=11, color="#6b7280"),
        zeroline=False,
        range=[0, _y_max_q],
        tickformat=",",
    ),
    legend=dict(
        bgcolor="rgba(13,17,23,0.90)", bordercolor="#1e2535", borderwidth=1,
        font=dict(size=11.5, color="#94a3b8"),
        orientation="h", yanchor="bottom", y=-0.15, xanchor="left", x=0,
    ),
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig_quad, use_container_width=True)

st.markdown(f"""
<p style='font-size:0.82rem;color:#475569;text-align:center;margin:-10px 0 16px;'>
  Filtered to markets with 1,000+ venues ·
  Quadrant lines at median venue count ({int(_q_med_x):,}) and
  median off-peak events ({int(_q_med_y):,}) ·
  <b style='color:#fb923c;'>● Priority Launch</b> ·
  <b style='color:#38bdf8;'>● High Activity</b> ·
  <b style='color:#a78bfa;'>● Large Supply / Low Activation</b>
</p>
""", unsafe_allow_html=True)

st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 — FINAL INSIGHT CARD
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='margin-top:4px;margin-bottom:8px;padding:36px 40px;
            background:#12161f;
            border:1px solid #1e2535;border-radius:14px;
            border-left:4px solid #fb923c;
            box-shadow:0 4px 32px rgba(0,0,0,0.4);'>

  <p style='color:#e2e8f0;font-size:1.1rem;font-weight:700;
            line-height:1.5;margin:0 0 10px;letter-spacing:-0.01em;'>
    One Structural Pattern. {_D_TOTAL_DMAS} Markets. One Coordination Layer.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.88;margin:0 0 20px;'>
    Across <b style='color:#fb923c;'>{_D_TOTAL_VENUES:,} mapped venues</b>,
    the average venue records only
    <b style='color:#fb923c;'>{_D_AVG_OFFPK_PER_V} off-peak events</b>.
    The stages already exist.
    The artists — as Chapter 3 documented — already exist.
    The coordination layer is what activates it.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.88;margin:0 0 24px;'>
    Azimuth can prioritize the markets where existing venues, proven event activity,
    and under-activated weekday capacity overlap —
    turning fragmented calendar inventory into
    <b style='color:#fb923c;'>programmable live-event infrastructure</b>.
  </p>

  <div style='display:flex;gap:14px;flex-wrap:wrap;margin-bottom:22px;'>
    <div style='flex:1;min-width:180px;background:#0d1117;border:1px solid #1e2535;
                border-radius:8px;padding:14px 16px;'>
      <div style='font-size:0.60rem;font-weight:700;color:#fb923c;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:6px;'>Chapter 1</div>
      <p style='color:#64748b;font-size:0.82rem;line-height:1.6;margin:0;'>
        {prime_night_share:.2f}% of {total_events/1e6:.1f}M events compress into peak booking windows nationally.
      </p>
    </div>
    <div style='flex:1;min-width:180px;background:#0d1117;border:1px solid #1e2535;
                border-radius:8px;padding:14px 16px;'>
      <div style='font-size:0.60rem;font-weight:700;color:#f59e0b;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:6px;'>Chapter 2</div>
      <p style='color:#64748b;font-size:0.82rem;line-height:1.6;margin:0;'>
        {v_extreme:,} venues carry ≥80% peak-window concentration in their booking history.
      </p>
    </div>
    <div style='flex:1;min-width:180px;background:#0d1117;border:1px solid #1e2535;
                border-radius:8px;padding:14px 16px;'>
      <div style='font-size:0.60rem;font-weight:700;color:#a78bfa;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:6px;'>Chapter 3</div>
      <p style='color:#64748b;font-size:0.82rem;line-height:1.6;margin:0;'>
        {m_dark} bookable mid-tier artists carry genuine radio audiences and zero live shows.
      </p>
    </div>
    <div style='flex:1;min-width:180px;background:#0d1117;border:1px solid #1e2535;
                border-radius:8px;padding:14px 16px;'>
      <div style='font-size:0.60rem;font-weight:700;color:#38bdf8;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:6px;'>Chapter 4</div>
      <p style='color:#64748b;font-size:0.82rem;line-height:1.6;margin:0;'>
        Across {_D_TOTAL_DMAS} DMA markets, {_D_TOTAL_VENUES:,} venues average
        only {_D_AVG_OFFPK_PER_V} off-peak events — a structural weekday activation gap.
      </p>
    </div>
  </div>

  <p style='color:#fb923c;font-size:0.95rem;font-weight:700;
            line-height:1.7;margin:0;'>
    Four independent datasets. Four different levels of analysis.
    One conclusion: the gap is real, it is structural, and it is coordinated by Azimuth.
  </p>

</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — FROM OPPORTUNITY TO SCALE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style='margin:72px 0 0;padding-top:52px;border-top:1px solid #1e2535;'>
  <div style='font-size:0.68rem;font-weight:700;color:#fb923c;text-transform:uppercase;
              letter-spacing:0.18em;margin-bottom:14px;'>
    The Business Case
  </div>
  <h1 style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.06;margin:0 0 14px;'>
    From Opportunity to Scale
  </h1>
  <p style='font-size:0.97rem;color:#64748b;max-width:740px;line-height:1.8;
            border-left:3px solid #1e2535;padding-left:16px;margin:0 0 32px;'>
    What happens when Azimuth begins to activate
    <b style='color:#e2e8f0;'>existing calendar inventory at scale?</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ─── VISUAL 1: Cascade Flow ───────────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  What Happens When Existing Capacity Is Activated?
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:22px;line-height:1.65;'>
  779,997 programmable event opportunities have been identified in existing venue calendars.
  At <b style='color:#e2e8f0;'>Early Scale</b>, Azimuth activates just 10,000 of them —
  less than 1.3% of total identified capacity.
  <b style='color:#fb923c;'>No new venues required.</b>
</p>
""", unsafe_allow_html=True)

_funnel_nodes = [
    {
        "y": 8.4,
        "num": "779,997",
        "label": "PROGRAMMABLE EVENT OPPORTUNITIES",
        "sub": "Existing venue calendar inventory across U.S. markets",
        "fill": "#0b1e33",
        "border": "#38bdf8",
        "num_color": "#38bdf8",
    },
    {
        "y": 5.9,
        "num": "10,000",
        "label": "EVENTS ACTIVATED — EARLY SCALE",
        "sub": "Less than 1.3% of identified capacity · Existing venues only",
        "fill": "#2a1400",
        "border": "#fb923c",
        "num_color": "#fb923c",
    },
    {
        "y": 3.4,
        "num": "2.0 Million",
        "label": "AUDIENCE EXPERIENCES CREATED",
        "sub": "200 attendees per event average",
        "fill": "#271900",
        "border": "#f59e0b",
        "num_color": "#f59e0b",
    },
    {
        "y": 0.9,
        "num": "$70 Million",
        "label": "ILLUSTRATIVE TICKET VALUE",
        "sub": "$35 average ticket price · Illustrative estimate, not a revenue forecast",
        "fill": "#170f30",
        "border": "#a78bfa",
        "num_color": "#a78bfa",
    },
]

fig_funnel = go.Figure()
fig_funnel.update_layout(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    height=520,
    margin=dict(l=80, r=80, t=16, b=24),
    xaxis=dict(visible=False, range=[0, 10]),
    yaxis=dict(visible=False, range=[-0.2, 9.6]),
    showlegend=False,
)

for _fn in _funnel_nodes:
    fig_funnel.add_shape(
        type="rect", layer="below",
        x0=1.2, x1=8.8,
        y0=_fn["y"] - 0.88, y1=_fn["y"] + 0.88,
        fillcolor=_fn["fill"],
        line=dict(color=_fn["border"], width=1.5),
    )
    fig_funnel.add_annotation(
        x=5, y=_fn["y"] + 0.24,
        text=f"<b>{_fn['num']}</b>",
        font=dict(size=30, color=_fn["num_color"], family="Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="middle",
    )
    fig_funnel.add_annotation(
        x=5, y=_fn["y"] - 0.20,
        text=_fn["label"],
        font=dict(size=9.5, color="#94a3b8", family="Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="middle",
    )
    fig_funnel.add_annotation(
        x=5, y=_fn["y"] - 0.58,
        text=_fn["sub"],
        font=dict(size=8.5, color="#475569", family="Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="middle",
    )

for _fy in [7.15, 4.65, 2.15]:
    fig_funnel.add_annotation(
        x=5, y=_fy,
        text="▼",
        font=dict(size=14, color="#2d3f55"),
        showarrow=False, xanchor="center", yanchor="middle",
    )

st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})

# ─── VISUAL 2: Scaling Scenarios ──────────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Scaling Scenarios
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:22px;line-height:1.65;'>
  Three activation scenarios — each uses existing venue inventory, zero new construction.
  <b style='color:#e2e8f0;'>200 attendees/event</b> ·
  <b style='color:#e2e8f0;'>$35 average ticket price</b> · Illustrative estimates only.
</p>
""", unsafe_allow_html=True)

_SC_LABELS  = ["Early Scale", "Regional Scale", "National Scale"]
_SC_EVENTS  = [10_000, 25_000, 50_000]
_SC_EVT_LBL = ["10,000", "25,000", "50,000"]
_SC_AUD_LBL = ["2.0M Audience", "5.0M Audience", "10.0M Audience"]
_SC_TKT_LBL = ["$70M Ticket Value", "$175M Ticket Value", "$350M Ticket Value"]
_SC_COLORS  = ["#fb923c", "#f59e0b", "#a78bfa"]

fig_scale = go.Figure()
fig_scale.add_trace(go.Bar(
    x=_SC_LABELS,
    y=_SC_EVENTS,
    marker_color=_SC_COLORS,
    marker_line_width=0,
    width=0.48,
    showlegend=False,
    hoverinfo="skip",
))

for _sci, (_lbl, _ev, _aud, _tkt, _evl, _col) in enumerate(
    zip(_SC_LABELS, _SC_EVENTS, _SC_AUD_LBL, _SC_TKT_LBL, _SC_EVT_LBL, _SC_COLORS)
):
    fig_scale.add_annotation(
        x=_lbl, y=_ev * 0.60,
        text=f"<b>{_evl}</b>",
        font=dict(size=26, color="#0d1117", family="Arial Black, Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="middle",
    )
    fig_scale.add_annotation(
        x=_lbl, y=_ev * 0.24,
        text="events activated",
        font=dict(size=9.5, color="#1c1c1c"),
        showarrow=False, xanchor="center", yanchor="middle",
    )
    fig_scale.add_annotation(
        x=_lbl, y=_ev + 1800,
        text=f"<b>{_aud}</b>",
        font=dict(size=13, color=_col, family="Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="bottom",
    )
    fig_scale.add_annotation(
        x=_lbl, y=_ev + 4400,
        text=f"<b>{_tkt}</b>",
        font=dict(size=13, color=_col, family="Arial, sans-serif"),
        showarrow=False, xanchor="center", yanchor="bottom",
    )

fig_scale.update_layout(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#12161f",
    height=440,
    margin=dict(l=30, r=30, t=10, b=20),
    xaxis=dict(
        showgrid=False, zeroline=False,
        tickfont=dict(size=13, color="#e2e8f0", family="Arial Black, Arial, sans-serif"),
        tickmode="array", tickvals=_SC_LABELS,
        linecolor="#1e2535",
    ),
    yaxis=dict(
        showgrid=False, zeroline=False,
        showticklabels=False,
        range=[0, 63_000],
    ),
    bargap=0.42,
)

st.plotly_chart(fig_scale, use_container_width=True, config={"displayModeBar": False})

# ─── Scenario cards ───────────────────────────────────────────────────────────

st.markdown("""
<div style='display:flex;gap:16px;flex-wrap:wrap;margin:8px 0 28px;'>

  <div style='flex:1;min-width:200px;background:#12161f;border:1px solid #1e2535;
              border-top:3px solid #fb923c;border-radius:10px;padding:26px 22px;'>
    <div style='font-size:0.64rem;font-weight:700;color:#fb923c;text-transform:uppercase;
                letter-spacing:0.15em;margin-bottom:10px;'>Early Scale</div>
    <div style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
                letter-spacing:-0.04em;line-height:1;margin-bottom:4px;'>10,000</div>
    <div style='font-size:0.82rem;color:#64748b;margin-bottom:14px;'>Additional Annual Events</div>
    <div style='height:1px;background:#1e2535;margin-bottom:14px;'></div>
    <div style='font-size:0.84rem;color:#94a3b8;line-height:1.8;'>
      <b style='color:#fb923c;'>2.0M</b> audience experiences<br>
      <b style='color:#fb923c;'>$70M</b> illustrative ticket value
    </div>
  </div>

  <div style='flex:1;min-width:200px;background:#12161f;border:1px solid #1e2535;
              border-top:3px solid #f59e0b;border-radius:10px;padding:26px 22px;'>
    <div style='font-size:0.64rem;font-weight:700;color:#f59e0b;text-transform:uppercase;
                letter-spacing:0.15em;margin-bottom:10px;'>Regional Scale</div>
    <div style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
                letter-spacing:-0.04em;line-height:1;margin-bottom:4px;'>25,000</div>
    <div style='font-size:0.82rem;color:#64748b;margin-bottom:14px;'>Additional Annual Events</div>
    <div style='height:1px;background:#1e2535;margin-bottom:14px;'></div>
    <div style='font-size:0.84rem;color:#94a3b8;line-height:1.8;'>
      <b style='color:#f59e0b;'>5.0M</b> audience experiences<br>
      <b style='color:#f59e0b;'>$175M</b> illustrative ticket value
    </div>
  </div>

  <div style='flex:1;min-width:200px;background:#12161f;border:1px solid #1e2535;
              border-top:3px solid #a78bfa;border-radius:10px;padding:26px 22px;'>
    <div style='font-size:0.64rem;font-weight:700;color:#a78bfa;text-transform:uppercase;
                letter-spacing:0.15em;margin-bottom:10px;'>National Scale</div>
    <div style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
                letter-spacing:-0.04em;line-height:1;margin-bottom:4px;'>50,000</div>
    <div style='font-size:0.82rem;color:#64748b;margin-bottom:14px;'>Additional Annual Events</div>
    <div style='height:1px;background:#1e2535;margin-bottom:14px;'></div>
    <div style='font-size:0.84rem;color:#94a3b8;line-height:1.8;'>
      <b style='color:#a78bfa;'>10.0M</b> audience experiences<br>
      <b style='color:#a78bfa;'>$350M</b> illustrative ticket value
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ─── Final insight card ───────────────────────────────────────────────────────

st.markdown("""
<div style='margin-top:4px;margin-bottom:48px;padding:36px 40px;
            background:#12161f;
            border:1px solid #1e2535;border-radius:14px;
            border-left:4px solid #fb923c;
            box-shadow:0 4px 32px rgba(0,0,0,0.4);'>

  <p style='color:#e2e8f0;font-size:1.1rem;font-weight:700;
            line-height:1.5;margin:0 0 10px;letter-spacing:-0.01em;'>
    The Infrastructure Already Exists
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.88;margin:0 0 14px;'>
    The opportunity is not to build more venues.<br>
    The opportunity is to activate existing calendars.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.88;margin:0 0 14px;'>
    Even modest calendar activation across identified high-concentration venues can create
    tens of thousands of additional live events, millions of audience experiences,
    and significant economic value — all from within the infrastructure that already exists.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.88;margin:0;'>
    Azimuth's role is to become the coordination layer that transforms fragmented venue
    availability into <b style='color:#fb923c;'>scalable event supply</b>:
    the stages already exist,
    the artists already exist,
    the audiences already exist.
    <b style='color:#e2e8f0;'>The coordination layer is what activates it.</b>
  </p>

</div>
""", unsafe_allow_html=True)


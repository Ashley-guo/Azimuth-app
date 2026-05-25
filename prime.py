import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="The Venue Utilization Gap — Azimuth Chapter 1",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
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

/* KPI card */
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


# ── Data ───────────────────────────────────────────────────────────────────────

total_events      = 2_679_577
prime_night_events = 1_638_533
prime_night_share  = 61.15

weekday_data = pd.DataFrame({
    "weekday": [0, 1, 2, 3, 4, 5, 6],
    "day":     ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "total_events": [395124, 173669, 232569, 276839, 357967, 589658, 653751],
})
weekday_data["is_prime"]    = weekday_data["weekday"].isin([0, 5, 6])
weekday_data["event_share"] = weekday_data["total_events"] / total_events * 100

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_data["day"] = pd.Categorical(weekday_data["day"], categories=weekday_order, ordered=True)
weekday_data = weekday_data.sort_values("day").reset_index(drop=True)

avg_events = weekday_data["total_events"].mean()

@st.cache_data
def load_state_data():
    try:
        return pd.read_csv("state_summary.csv")
    except Exception:
        return None

state_df = load_state_data()


# ── Hero ───────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:16px 0 36px;'>

  <div style='font-size:0.72rem;font-weight:700;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.18em;margin-bottom:14px;'>
    Chapter 1
  </div>

  <h1 style='font-size:2.8rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.08;margin:0 0 12px;'>
    The Venue Utilization Gap
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


# ── KPI Cards ──────────────────────────────────────────────────────────────────

def kpi(val, lbl, accent):
    return (
        f"<div class='kpi-wrap' style='--accent:{accent};'>"
        f"<div class='kpi-num'>{val}</div>"
        f"<div class='kpi-sub'>{lbl}</div>"
        f"</div>"
    )

c1, c2, c3 = st.columns(3)
c1.markdown(kpi(f"{total_events:,}",   "Total Historical Events<br>in Dataset",             "#fb923c"), unsafe_allow_html=True)
c2.markdown(kpi(f"{prime_night_events:,}", "Events in Peak Booking Windows<br>Fri · Sat · Sun",     "#f59e0b"), unsafe_allow_html=True)
c3.markdown(kpi(f"{prime_night_share:.1f}%", "of All Events<br>in Just 3 Booking Windows",           "#a78bfa"), unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
non_prime = total_events - prime_night_events
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


# ── Chart 1 — Weekday Demand Bar Chart ─────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Live Entertainment Demand Concentrates Into Peak Booking Windows
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:2px;line-height:1.65;'>
  Event volume by day of week across 2.6M historical events.
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

# Prime zone background (Fri=4, Sat=5, Sun=6 → indices 3.5–6.5)
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

# Weekly average reference line
fig1.add_hline(
    y=avg_events,
    line=dict(color="#334155", width=1.5, dash="dot"),
    annotation_text=f"  Weekly avg  {avg_events:,.0f}",
    annotation_position="top right",
    annotation_font=dict(color="#64748b", size=11, family="Inter, sans-serif"),
)

# "PEAK ZONE" badge annotation
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

# Saturday peak callout
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
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=540,
    margin=dict(l=60, r=80, t=20, b=60),
    xaxis=dict(
        title=dict(text="Day of Week", font=dict(size=13, color="#64748b")),
        gridcolor="#0d1520",
        tickfont=dict(size=13, color="#94a3b8"),
        showgrid=False,
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Number of Events", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28",
        tickfont=dict(size=11, color="#6b7280"),
        zeroline=False,
        range=[0, weekday_data["total_events"].max() * 1.25],
    ),
    showlegend=False,
    hoverlabel=dict(
        bgcolor="#1a2133", bordercolor="#2e3a52",
        font=dict(size=12.5, family="Inter, sans-serif"),
    ),
)

st.plotly_chart(fig1, use_container_width=True)

# Two-card insight strip
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


# ── Chart 2 — Prime vs Non-Prime Donut ─────────────────────────────────────────

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Peak Booking Windows Capture the Majority of Live Event Activity
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:8px;line-height:1.65;'>
  Three booking windows vs. four — the demand concentration is not close.
</p>
""", unsafe_allow_html=True)

col_donut, col_dinsight = st.columns([1.25, 1])

with col_donut:
    fig2 = go.Figure(go.Pie(
        labels=["Peak Windows  (Fri / Sat / Sun)", "Off-Peak Windows  (Mon – Thu)"],
        values=[prime_night_events, non_prime],
        hole=0.65,
        marker=dict(
            colors=["#fb923c", "#1e2d45"],
            line=dict(color="#0d1117", width=4),
        ),
        pull=[0.04, 0],
        textinfo="percent",
        textfont=dict(family="Inter, sans-serif", size=13, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>Events: %{value:,}<br>Share: %{percent}<extra></extra>",
        sort=False,
    ))

    fig2.add_annotation(
        text=(
            f"<b>{prime_night_share:.1f}%</b><br>"
            "<span style='font-size:11px;color:#64748b;'>Peak-Window</span><br>"
            "<span style='font-size:11px;color:#64748b;'>Concentration</span>"
        ),
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(color="#fb923c", size=22, family="Inter, sans-serif"),
        xanchor="center", yanchor="middle", align="center",
    )

    fig2.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#94a3b8", family="Inter, sans-serif"),
        height=380,
        margin=dict(l=20, r=20, t=20, b=30),
        legend=dict(
            bgcolor="rgba(13,17,23,0.9)",
            bordercolor="#1e2535",
            borderwidth=1,
            font=dict(size=12, color="#94a3b8"),
            orientation="h",
            yanchor="bottom", y=-0.09,
            xanchor="center", x=0.5,
        ),
        hoverlabel=dict(
            bgcolor="#1a2133", bordercolor="#2e3a52",
            font=dict(size=12.5, family="Inter, sans-serif"),
        ),
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_dinsight:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-radius:10px;
                padding:24px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;
                  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:18px;'>
        What This Concentration Means
      </div>

      <div style='display:flex;gap:12px;margin-bottom:18px;'>
        <div style='width:3px;min-height:40px;border-radius:2px;
                    background:#fb923c;flex-shrink:0;'></div>
        <div>
          <div style='color:#fb923c;font-weight:700;font-size:0.9rem;
                      margin-bottom:5px;'>3 Peak Booking Windows</div>
          <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.65;margin:0;'>
            {prime_night_events:,} events on Fri, Sat &amp; Sun
            — <b>{prime_night_share:.1f}%</b> of all live activity.
          </p>
        </div>
      </div>

      <div style='display:flex;gap:12px;margin-bottom:22px;'>
        <div style='width:3px;min-height:40px;border-radius:2px;
                    background:#334155;flex-shrink:0;'></div>
        <div>
          <div style='color:#64748b;font-weight:700;font-size:0.9rem;
                      margin-bottom:5px;'>4 Off-Peak Windows</div>
          <p style='color:#94a3b8;font-size:0.87rem;line-height:1.65;margin:0;'>
            {non_prime:,} events on Mon–Thu
            — only <b>{100-prime_night_share:.1f}%</b> of all live activity.
          </p>
        </div>
      </div>

      <hr style='border:none;border-top:1px solid #1e2535;margin:0 0 16px;'>
      <p style='color:#94a3b8;font-size:0.87rem;line-height:1.75;margin:0;'>
        A venue with no bookings on Friday or Saturday is missing its
        highest-value inventory window — a systematic underutilization
        of peak-demand capacity.
        <b style='color:#fb923c;'>That is the gap Azimuth reactivates.</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ── Chapter 1 → Chapter 2 bridge card ─────────────────────────────────────────
# Sets up the question Chapter 2 answers: not just "weekends dominate" at the
# aggregate level, but "how concentrated is each venue's own calendar?"

st.markdown(f"""
<div style='padding:28px 32px;background:#12161f;border:1px solid #1e2535;
            border-radius:14px;border-left:4px solid #fb923c;
            box-shadow:0 4px 32px rgba(0,0,0,0.4);margin-bottom:8px;'>
  <p style='color:#e2e8f0;font-size:1.05rem;font-weight:500;
            line-height:1.85;margin:0 0 16px;'>
    Uber transformed <b>idle mobility capacity</b> into a coordinated transportation network.<br>
    Airbnb transformed <b>underutilized housing inventory</b> into bookable hospitality supply.<br>
    <span style='color:#fb923c;font-weight:700;'>Azimuth transforms under-activated venue calendars
    into programmable live-event infrastructure.</span>
  </p>
  <p style='color:#64748b;font-size:0.9rem;line-height:1.75;margin:0;'>
    With <b style='color:#fb923c;'>{prime_night_share:.1f}%</b> of all {total_events:,} live events
    concentrated in peak booking windows, the real opportunity is not in building more venues —
    it is in identifying which proven stages carry underutilized calendar capacity.
    <b style='color:#94a3b8;'>Chapter 2 maps exactly that gap at the venue level.</b>
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Venue Activity Is Concentrated Into Peak Booking Windows
# Data: venue_prime_night_dependence.csv
# Each venue has a prime_night_share (events on Fri/Sat/Sun ÷ total events).
# We show WHERE the distribution falls, WHICH venues are most locked in,
# and WHAT that means for Azimuth's addressable opportunity.
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np

@st.cache_data
def load_venue_prime():
    df = pd.read_csv("venue_prime_night_dependence.csv")
    df["venue_capacity"] = pd.to_numeric(df["venue_capacity"], errors="coerce")
    # Dependence tier — used for colour-coding throughout
    df["tier"] = pd.cut(
        df["prime_night_share"],
        bins=[-0.001, 40, 80, 100.001],
        labels=["Balanced  (<40%)", "Peak-Skewed  (40–80%)", "Extreme  (≥80%)"],
    )
    # Log-scaled bubble size; unknown/zero capacity gets a minimum dot
    df["cap_valid"] = df["venue_capacity"].fillna(0).clip(lower=0)
    df["bubble"]    = np.where(
        df["cap_valid"] > 0,
        np.clip(np.log1p(df["cap_valid"]) * 3.2, 7, 42),
        7,
    )
    df["cap_label"] = np.where(df["cap_valid"] > 0,
                               df["cap_valid"].astype(int).astype(str), "—")
    return df

vdf = load_venue_prime()

v_total    = len(vdf)
v_avg_prime = vdf["prime_night_share"].mean()
v_avg_off   = vdf["off_night_share"].mean()
v_extreme   = int((vdf["prime_night_share"] >= 80).sum())
v_extreme_pct = v_extreme / v_total * 100
v_balanced  = int((vdf["prime_night_share"] < 40).sum())


# ── Chapter 2 hero ─────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:8px 0 26px;'>
  <div style='font-size:0.78rem;font-weight:600;color:#4b5675;
              text-transform:uppercase;letter-spacing:0.14em;margin-bottom:10px;'>
    Chapter 2
  </div>
  <h1 style='font-size:2.6rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.04em;line-height:1.1;margin-bottom:14px;'>
    Venue Activity Is Concentrated Into Peak Booking Windows
  </h1>
  <p style='font-size:0.97rem;color:#64748b;max-width:720px;line-height:1.8;
            border-left:3px solid #1e2535;padding-left:16px;margin:0;'>
    Live entertainment infrastructure does not behave like evenly utilised real estate.
    Venue booking activity concentrates into a narrow set of peak windows, leaving large
    portions of the weekly calendar structurally under-activated.
    This is the same utilisation gap that made Uber and Airbnb transformative:
    <b style='color:#e2e8f0;'>existing assets were already there, but the market lacked a
    coordination layer to activate them efficiently.</b>
  </p>
</div>
""", unsafe_allow_html=True)

# Uber / Airbnb / Azimuth — three-panel thesis strip (st.columns for reliable rendering)
ub1, ub2, ub3 = st.columns(3)
with ub1:
    st.markdown("""
    <div style='background:#0f1420;border:1px solid #1e2535;border-radius:10px;
                padding:20px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#334155;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>Uber</div>
      <p style='color:#94a3b8;font-size:0.9rem;line-height:1.7;margin:0;'>
        Did not manufacture cars.<br>
        It identified <b style='color:#cbd5e1;'>idle mobility capacity</b>
        and built a coordination layer to deploy it on demand.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ub2:
    st.markdown("""
    <div style='background:#0f1420;border:1px solid #1e2535;border-radius:10px;
                padding:20px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#334155;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>Airbnb</div>
      <p style='color:#94a3b8;font-size:0.9rem;line-height:1.7;margin:0;'>
        Did not build hotels.<br>
        It identified <b style='color:#cbd5e1;'>underutilized housing inventory</b>
        and turned latent supply into bookable hospitality.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ub3:
    st.markdown("""
    <div style='background:#16100a;border:2px solid #fb923c;border-radius:10px;
                padding:20px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.62rem;font-weight:700;color:#c2410c;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:10px;'>Azimuth</div>
      <p style='color:#fb923c;font-size:0.9rem;line-height:1.7;margin:0;font-weight:600;'>
        Does not build venues.<br>
        It coordinates <b>under-activated venue calendars</b>
        and converts fragmented booking capacity into programmable live-event infrastructure.
      </p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

st.divider()


# ── Chapter 2 KPI Cards ────────────────────────────────────────────────────────

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


# ── Data Methodology — the most important analytical decision in this chapter ──
# Without this explanation, a reader might assume the weekend concentration
# is just a trivial artefact of festival records.  We need to show it isn't.

st.markdown("""
<div style='margin-bottom:32px;'>
  <h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
             letter-spacing:-0.02em;margin-bottom:8px;'>
    How This Dataset Was Constructed — And Why It Matters
  </h2>
  <p style='font-size:0.88rem;color:#64748b;margin-bottom:0;line-height:1.7;'>
    The first version of this query returned festival records at the top of every ranking.
    That raw result was analytically worthless — and here is why.
  </p>
</div>
""", unsafe_allow_html=True)

# Two-column layout: problem on the left, solution + implication on the right
mc1, mc2 = st.columns([1, 1])

with mc1:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #334155;
                border-radius:10px;padding:22px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:14px;'>
        The Problem With Raw Data
      </div>

      <p style='color:#94a3b8;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        Entities like <b style='color:#e2e8f0;'>Coachella, Lollapalooza, Austin City Limits,
        Boston Calling</b> — and any record tagged "Festival," "Parade," or "Tour" —
        are <b style='color:#e2e8f0;'>structurally 100% weekend-only by design</b>.
        They were built that way. Their peak-window concentration tells us nothing
        about the live venue market; it is simply a scheduling artefact baked into
        their format.
      </p>

      <p style='color:#94a3b8;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        Including them would make the conclusion trivially obvious and analytically useless —
        like measuring hotel occupancy by only counting resort weekends, then concluding
        "hotels are weekend businesses."
      </p>

    </div>
    """, unsafe_allow_html=True)

with mc2:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:10px;padding:22px 22px;height:100%;box-sizing:border-box;'>
      <div style='font-size:0.65rem;font-weight:700;color:#c2410c;text-transform:uppercase;
                  letter-spacing:0.12em;margin-bottom:14px;'>
        What Remains — And Why The Finding Is Stronger
      </div>

      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        After filtering, the remaining <b style='color:#fb923c;'>17,315 venues</b> are
        <b style='color:#e2e8f0;'>ordinary recurring live entertainment infrastructure</b>:
        clubs, theaters, concert halls, arenas, ballrooms — venues that could
        in principle host events on any day of the week.
      </p>

      <p style='color:#cbd5e1;font-size:0.87rem;line-height:1.75;margin:0 0 14px;'>
        These venues have no scheduling constraint forcing them into weekends.
        And yet the pattern holds: <b style='color:#fb923c;'>their booking activity is still
        heavily concentrated on Friday, Saturday, and Sunday</b>.
        That is the structural story — not imposed by format, but by how the
        live entertainment market has historically operated without a coordination layer.
      </p>

      <div style='background:#1a0e00;border:1px solid #fb923c;border-radius:6px;
                  padding:12px 14px;font-size:0.87rem;color:#fb923c;line-height:1.7;'>
        <b>This makes the conclusion more conservative, not less.</b>
        If even non-festival venues show 62% average peak-window concentration,
        the utilisation gap is real — and Azimuth's opportunity is structural.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# CHART A — Peak-Window Concentration Curve (histogram)
# Question answered: "How many venues are structurally locked into peak windows?"
# Three shaded zones make the answer immediately legible.
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Peak-Window Concentration Curve
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  How to read this chart: every bar is a bucket of venues sharing a similar peak-window concentration.
  Bars toward the <b style='color:#38bdf8;'>left (blue)</b> = venues whose bookings spread relatively
  evenly across the week. Bars toward the <b style='color:#fb923c;'>right (orange)</b> = venues
  whose booking activity is almost entirely concentrated into Friday–Sunday.
  <b style='color:#e2e8f0;'>The shape of this curve is the shape of Azimuth's opportunity.</b>
</p>
""", unsafe_allow_html=True)

bins_h      = np.arange(0, 105, 5)
hist_vals, bin_edges = np.histogram(vdf["prime_night_share"], bins=bins_h)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
y_ceil      = hist_vals.max() * 1.32

# Bars coloured by zone so the three regions are immediately readable
bar_clr = []
for c in bin_centers:
    if c < 40:
        bar_clr.append("#1e3a5f")   # muted blue  — Balanced
    elif c < 80:
        bar_clr.append("#78350f")   # dark amber  — Peak-Skewed
    else:
        bar_clr.append("#fb923c")   # orange      — Extreme

fig_hist = go.Figure()

# Zone backgrounds drawn behind bars
for x0, x1, fill in [
    (0,  40,  "rgba(56,189,248,0.035)"),
    (40, 80,  "rgba(245,158,11,0.05)"),
    (80, 100, "rgba(251,146,60,0.08)"),
]:
    fig_hist.add_shape(type="rect", layer="below",
                       x0=x0, x1=x1, y0=0, y1=y_ceil,
                       fillcolor=fill, line_width=0)

# Zone divider lines
for xv, col in [(40, "#1e3a5f"), (80, "rgba(251,146,60,0.5)")]:
    fig_hist.add_shape(type="line", layer="below",
                       x0=xv, x1=xv, y0=0, y1=y_ceil * 0.96,
                       line=dict(color=col, width=1.2, dash="dot"))

fig_hist.add_trace(go.Bar(
    x=bin_centers,
    y=hist_vals,
    width=4.3,
    marker=dict(color=bar_clr, opacity=0.9,
                line=dict(color="rgba(0,0,0,0.25)", width=0.4)),
    hovertemplate=(
        "Peak-Window Concentration: <b>%{x:.0f}%</b><br>"
        "Venues: <b>%{y:,}</b><extra></extra>"
    ),
))

# 80 % threshold — the key investor reference line
fig_hist.add_annotation(
    x=80, y=y_ceil * 0.93,
    text="<b>80% Threshold</b><br>Extreme Peak-Window Concentration",
    showarrow=True, arrowhead=2, arrowcolor="rgba(251,146,60,0.7)",
    arrowwidth=1.5, ax=56, ay=0,
    font=dict(size=11.5, color="#fb923c", family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.88)",
    bordercolor="rgba(251,146,60,0.40)",
    borderpad=8, borderwidth=1,
    xanchor="left",
)

# Zone label badges — one per region
for x_mid, label, color, bg in [
    (20, "BALANCED",     "#38bdf8", "rgba(56,189,248,0.10)"),
    (60, "PEAK-SKEWED",  "#f59e0b", "rgba(245,158,11,0.10)"),
    (90, "EXTREME",      "#fb923c", "rgba(251,146,60,0.14)"),
]:
    fig_hist.add_annotation(
        x=x_mid, y=y_ceil * 0.82,
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=11, color=color, family="Inter, sans-serif"),
        xanchor="center",
        bgcolor=bg,
        bordercolor=color,
        borderpad=6, borderwidth=1,
    )

# Annotate the histogram peak bin
peak_idx   = hist_vals.argmax()
peak_x     = bin_centers[peak_idx]
peak_count = hist_vals[peak_idx]
fig_hist.add_annotation(
    x=peak_x, y=peak_count,
    text=f"<b>{peak_count:,} venues</b><br>most common range",
    showarrow=True, arrowhead=2,
    arrowcolor="#6b7a99", arrowwidth=1.2,
    ax=0, ay=-52,
    font=dict(size=10.5, color="#94a3b8", family="Inter, sans-serif"),
    bgcolor="rgba(13,17,23,0.80)",
    bordercolor="#1e2535", borderpad=6, borderwidth=1,
)

fig_hist.update_layout(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=460,
    margin=dict(l=65, r=70, t=24, b=65),
    xaxis=dict(
        title=dict(text="Peak-Window Concentration  (%)", font=dict(size=13, color="#64748b")),
        range=[0, 101], dtick=10,
        tickfont=dict(size=12, color="#94a3b8"),
        gridcolor="#0d1520", zeroline=False, showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Number of Venues", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28",
        tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, y_ceil],
    ),
    showlegend=False, bargap=0.12,
    hoverlabel=dict(bgcolor="#1a2133", bordercolor="#2e3a52",
                    font=dict(size=12.5, family="Inter, sans-serif")),
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown(f"""
<p style='font-size:0.82rem;color:#475569;text-align:center;margin:-12px 0 16px;'>
  Festival and one-off entities excluded · Minimum 20 historical events per venue ·
  <b style='color:#fb923c;'>{v_extreme:,} venues ({v_extreme_pct:.0f}%)</b> above the 80% line
</p>
""", unsafe_allow_html=True)

# ── Histogram interpretation — use st.columns so Streamlit renders reliably ────
st.markdown("""
<div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
            letter-spacing:0.12em;margin-bottom:10px;margin-top:4px;'>
  Reading This Chart
</div>
""", unsafe_allow_html=True)

ri1, ri2, ri3 = st.columns(3)
with ri1:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #38bdf8;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#38bdf8;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Balanced  &lt;40%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        Only <b style='color:#38bdf8;'>{v_balanced:,} venues</b> here.
        These stages generate bookings consistently across the week —
        more like a restaurant with steady covers every day than a
        venue that only activates on Saturday. Rare in this market.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ri2:
    st.markdown("""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#f59e0b;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Peak-Skewed  40–80%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        The largest zone. These venues lean toward weekends but still hold
        some weekday booking activity — partial utilisation, with portions
        of their calendar still under-activated.
        Most booking platforms treat these as "fully used" when in fact
        significant off-peak inventory remains uncaptured.
      </p>
    </div>
    """, unsafe_allow_html=True)
with ri3:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='color:#fb923c;font-weight:700;font-size:0.88rem;margin-bottom:6px;'>
        Extreme  ≥80%
      </div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        <b style='color:#fb923c;'>{v_extreme:,} venues</b> — {v_extreme_pct:.0f}% of the market.
        4 out of every 5 events fall within just three booking windows.
        Their Mon–Thu calendar represents structurally underutilized inventory.
        <b style='color:#e2e8f0;'>This is Azimuth's primary target segment.</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

# Two-card strip — mirrors the Chapter 1 style so the two halves feel unified
h_ia, h_ib = st.columns(2)
with h_ia:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:8px;padding:18px 20px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:8px;'>Extreme Zone  (≥80% Peak-Window)</div>
      <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.7;margin:0;'>
        <b style='color:#fb923c;'>{v_extreme:,} venues</b> concentrate 80%+ of all events into Fri–Sun.
        Like a hotel that fills every room on weekends but runs near-empty Mon–Thu —
        <b>monetising only a fraction of available inventory.</b>
      </p>
    </div>
    """, unsafe_allow_html=True)
with h_ib:
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #475569;
                border-radius:8px;padding:18px 20px;'>
      <div style='font-size:0.68rem;font-weight:600;color:#4b5675;text-transform:uppercase;
                  letter-spacing:0.08em;margin-bottom:8px;'>Balanced Zone  (&lt;40% Peak-Window)</div>
      <p style='color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0;'>
        Only <b style='color:#38bdf8;'>{v_balanced:,} venues</b>
        ({v_balanced / v_total * 100:.0f}% of the market) distribute bookings
        relatively evenly across the week.
        Peak-window concentration is the structural norm, not the exception.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# CHART B — Bubble Scatter: "Where Venue Activity Becomes Peak-Window Locked"
# x = total event history (proven operational track record)
# y = prime-night share  (how concentrated that history is)
# bubble = venue capacity (scale of the asset — log-normalised)
# colour = dependence tier
# Upper-right = high-history + peak-locked → Azimuth's primary target segment
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Where Venue Activity Becomes Peak-Window Locked
</h2>
<p style='font-size:0.88rem;color:#64748b;margin-bottom:6px;line-height:1.65;'>
  How to read this chart: move <b style='color:#e2e8f0;'>right</b> along the x-axis
  and a venue has more historical events — a longer operational track record.
  Move <b style='color:#fb923c;'>up</b> along the y-axis and more of that history
  is concentrated into peak booking windows. Bubble size reflects venue capacity.
  The <b style='color:#fb923c;'>upper-right corner</b> is the most commercially important zone:
  venues that are proven, high-capacity, <i>and</i> structurally concentrated into three booking windows.
  That is where under-activated calendar capacity is most valuable.
</p>
""", unsafe_allow_html=True)

# Cap x at 97th-percentile so a handful of mega-venues don't compress everyone else
x_cap    = int(vdf["total_events"].quantile(0.97))
plot_vdf = vdf[vdf["total_events"] <= x_cap].copy()

# Keep all high-event venues; random-sample the long tail for render performance
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

# 80 % threshold — soft background fill above the line
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

# Callout box in the top-right — Azimuth's target zone
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
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    height=540,
    margin=dict(l=70, r=40, t=20, b=100),
    xaxis=dict(
        title=dict(text="Total Historical Events  (capped at 97th-percentile for readability)",
                   font=dict(size=12, color="#64748b")),
        gridcolor="#0d1520",
        tickfont=dict(size=11, color="#6b7280"),
        zeroline=False, range=[0, x_cap * 1.04], showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Peak-Window Concentration  (%)", font=dict(size=13, color="#64748b")),
        gridcolor="#131a28",
        tickfont=dict(size=11, color="#6b7280"),
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

# ── Scatter interpretation ─────────────────────────────────────────────────────
# A chart without interpretation is just decoration. Tell the reader what
# the pattern means, not just what the axes show.
sc_ia, sc_ib, sc_ic = st.columns(3)
with sc_ia:
    st.markdown(f"""
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
    st.markdown(f"""
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
    st.markdown(f"""
    <div style='background:#12161f;border:1px solid #1e2535;border-top:2px solid #fb923c;
                border-radius:8px;padding:16px 18px;'>
      <div style='font-size:0.65rem;font-weight:700;color:#c2410c;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:8px;'>Upper-Right — Peak-Window Locked</div>
      <p style='color:#94a3b8;font-size:0.84rem;line-height:1.65;margin:0;'>
        High event history. High peak-window concentration. Large bubbles signal significant
        capacity. <b style='color:#fb923c;'>These are Azimuth's primary targets</b>:
        venues that have proven they can run shows, attract audiences, and fill seats —
        but whose off-peak calendar represents untapped, bookable inventory.
      </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# LEADERBOARD — Top 25 Most Peak-Window Concentrated Venues
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<h2 style='font-size:1.5rem;font-weight:800;color:#e2e8f0;
           letter-spacing:-0.02em;margin-bottom:4px;'>
  Most Peak-Window Concentrated Venues
</h2>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:#12161f;border:1px solid #1e2535;border-left:3px solid #f59e0b;
            border-radius:8px;padding:18px 24px;margin-bottom:16px;'>
  <div style='font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;
              letter-spacing:0.12em;margin-bottom:10px;'>How to Interpret This Table</div>
  <p style='color:#cbd5e1;font-size:0.88rem;line-height:1.8;margin:0 0 10px;'>
    These are venues with <b style='color:#e2e8f0;'>100% (or near-100%) peak-window
    concentration and meaningful event histories</b> — they are not data anomalies.
    They appear in years of historical booking records, which means they have
    operational capability, audience relationships, and proven event-running infrastructure.
  </p>
  <p style='color:#94a3b8;font-size:0.87rem;line-height:1.8;margin:0 0 10px;'>
    And yet: their off-peak booking column is near zero.
    That is not because no audience exists on a Tuesday —
    it is because <b style='color:#e2e8f0;'>no coordination layer has ever systematically
    activated that inventory at these venues</b>.
    The demand signal has never been tested. The capacity has never been deployed.
  </p>
  <p style='color:#94a3b8;font-size:0.87rem;line-height:1.8;margin:0 0 10px;'>
    <b style='color:#f59e0b;'>Note on data cleaning:</b> festival-heavy entities (Coachella,
    Lollapalooza, Austin City Limits, Boston Calling, Parades, Tours) were removed via
    keyword filters before building this dataset.
    Those records are structurally weekend-only by design — including them would have made
    the conclusion trivially obvious. <b style='color:#e2e8f0;'>What you see here are ordinary
    recurring venues</b>, not one-off events. That is precisely what makes this finding significant.
  </p>
  <p style='color:#fb923c;font-size:0.87rem;line-height:1.8;margin:0;font-weight:600;'>
    Their off-peak calendar inventory is effectively unsold. Azimuth is the coordination layer that activates it.
  </p>
</div>
""", unsafe_allow_html=True)

# Sort: highest prime share first; break ties by total events (more proven = higher)
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


# ── Closing Insight Card — Azimuth thesis made concrete with real numbers ──────

st.markdown(f"""
<div style='margin-top:4px;margin-bottom:8px;padding:32px 38px;
            background:#12161f;
            border:1px solid #1e2535;border-radius:14px;
            border-left:4px solid #fb923c;
            box-shadow:0 4px 32px rgba(0,0,0,0.4);'>

  <p style='color:#e2e8f0;font-size:1.1rem;font-weight:700;
            line-height:1.5;margin:0 0 10px;letter-spacing:-0.01em;'>
    The issue is not venue scarcity. The issue is calendar utilization inefficiency.
  </p>

  <p style='color:#94a3b8;font-size:0.92rem;line-height:1.85;margin:0 0 18px;'>
    Uber did not build more cars —
    it built a coordination layer for <i>idle mobility capacity</i>.<br>
    Airbnb did not build more hotels —
    it built a coordination layer for <i>underutilized housing inventory</i>.<br>
    <b style='color:#fb923c;'>Azimuth does not build venues —
    it coordinates under-activated venue calendars and turns fragmented booking capacity
    into programmable live-event infrastructure.</b>
  </p>

  <p style='color:#64748b;font-size:0.9rem;line-height:1.8;margin:0;'>
    Across {v_total:,} established venues,
    <b style='color:#fb923c;'>{v_extreme:,} ({v_extreme_pct:.0f}%)</b>
    concentrate 80% or more of their events into a single three-window period.
    Their Monday-through-Thursday calendars are structurally underutilized —
    not because demand is absent, but because no coordination layer has ever existed
    to activate it efficiently.<br><br>
    The infrastructure already exists. The opportunity is to coordinate when, where,
    and how that infrastructure gets activated —
    converting <b style='color:#fb923c;'>latent venue capacity into recurring,
    monetisable live-event inventory</b>.
    The stages are already built. The audiences are already there.
    What has been missing is the intelligence layer that connects them.
  </p>

</div>
""", unsafe_allow_html=True)

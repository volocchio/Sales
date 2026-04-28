# Tamarack Mission Analysis — Quick Start Guide for Sales

_From zero to your first mission simulation in under 10 minutes. Built for sales reps, not engineers._

---

## What it is

The **Tamarack Mission Analysis** simulator runs real flight physics for any Citation (CJ, CJ1/+, CJ2/+, CJ3/+, M2) on any route in the world, comparing **Flatwing (stock) vs. Tamarack (SMARTWING™)** side-by-side. It is the most powerful sales-conversation tool we have because it answers the prospect's actual question — *"What does this do for **my** missions?"* — with verifiable physics, not marketing math.

Use it on the call. Use it in the proposal. Use it on the demo flight debrief.

---

## 1 · Open the simulator

The tool is hosted on our VPS — no install required.

**→ [https://mission-analysis.voloaltro.tech](https://mission-analysis.voloaltro.tech)**

Bookmark it. If the page is slow to load the first time, it is the container warming up; refresh after ~10 seconds.

---

## 2 · Choose your mode

At the top of the page you'll see six mode tabs:

| Mode | What it does | When to use it |
|------|-------------|----------------|
| **Normal** | Run a single flight simulation | 90% of sales calls — start here |
| **Batch Sweeps** | Payload-range diagrams across multiple configs | Custom one-pagers / proposals |
| **WAT Charts** | Weight-Altitude-Temperature dispatch analysis | "Can I get out of Aspen in July?" |
| **ETOPS Analysis** | Engine-out diversion / overwater route planning | Bahamas, Caribbean, transatlantic prospects |
| **Build a Route** | Multi-leg route construction | Charter ops with multi-stop days |
| **Fleet Analysis** | Compare configs across a fleet | Fleet operators, multiple tails |

For your first run, stay on **Normal**.

---

## 3 · Set up a basic flight (Normal Mode)

### Interface selection
At the top, make sure **Main Simulator** is selected (not Aircraft Config Editor).

### Choose run mode
- **Single** — one aircraft configuration
- **Compare** — Flatwing vs. Tamarack side-by-side ← **always pick this for sales**

### Sidebar — flight parameters

**Step 1: Pick the aircraft**
- Select a weight group (Light ≤ 20k lb covers all Citations)
- Choose the Aircraft Model (CJ, CJ1, CJ1+, CJ2, CJ2+, CJ3, CJ3+, M2)
- In Compare mode, Side A defaults to Flatwing and Side B to Tamarack

**Step 2: Set the route**
- Type an ICAO code, city name, or airport name in the **Departure Airport** search box
- Do the same for **Arrival Airport**
- Example: `KTEB` → `KPBI` (Teterboro to Palm Beach)

**Step 3: Set weights**
- **Weight Option: "Max Fuel"** is the simplest starting point
- Adjust payload (passengers + bags) — typical: 400–800 lb for 2–4 pax
- Leave reserve and taxi fuel at defaults unless the prospect specifies otherwise

**Step 4: Set cruise**
- Cruise altitude: FL350–FL450 depending on model (FL410 is the sweet spot for CJ2+/CJ3)
- Cruise mode: "Constant Mach" is standard; use the aircraft's default Mach

**Step 5: Run it**
- Click **Run Simulation** at the bottom of the sidebar
- Results appear in the main panel: route map, altitude profile, fuel burn, distance, time

---

## 4 · Reading the results

The output shows a comparison table with the numbers that close deals:

| Metric | What to look for |
|--------|-----------------|
| **Total Range (nm)** | Tamarack goes further — highlight the extra range |
| **Total Fuel Burned (lb)** | Tamarack burns less — calculate annual savings |
| **Cruise Fuel Flow (pph)** | Lower = better; the % difference is your pitch |
| **Time to Cruise Alt** | Tamarack climbs faster to higher altitudes |
| **Fuel Remaining (lb)** | More reserve = more safety margin or more payload |

The route map shows the ground track. The altitude profile shows climb / cruise / descent. Hourly fuel-burn tables are included.

---

## 5 · Quick sales scenarios

### "Can I make it nonstop?"
Set the prospect's home base and their dream destination. Run Compare mode. If Flatwing can't make it (0 fuel remaining or negative) but Tamarack can — that's your pitch.

### "How much fuel will I save?"
Run any route in Compare mode. Take the fuel difference, multiply by price per gallon (Jet-A ÷ 6.7 lb/gal), multiply by annual hours. That's the annual savings number.

### "Can I dispatch from Aspen on a hot day?"
Switch to **WAT Charts** mode. Select the prospect's aircraft model. Set the airport to KASE (7,820 ft). Increase OAT. Show where the Flatwing MTOW drops but Tamarack holds.

### "Bahamas with two pilots and four pax"
Switch to **ETOPS Analysis**. Set departure (KFXE/KOPF), arrival (MYNN/MYAT), payload, and overwater diversion fields. Tamarack typically opens up direct routings the Flatwing can't.

---

## 6 · Saving & sharing results

- Simulation outputs are saved server-side to the `output/` folder with timestamps
- CSV time-history data is generated automatically
- Charts can be downloaded directly from the Plotly toolbar (camera icon → PNG) — drop them into proposals
- Use **Batch Sweeps** mode to generate payload-range charts for one-pagers and proposals

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Page won't load | Wait 15 seconds and refresh — the container may be cold-starting |
| Airport not found | Use the 4-letter ICAO code (e.g., `KTEB`), not the FAA 3-letter |
| Simulation seems slow | Normal — physics runs at 1-second timesteps; long routes take 10–30 seconds |
| Numbers look wrong | Check payload, fuel option, and cruise altitude settings; defaults are conservative |
| Need a config the dropdown doesn't have | Ping Nick or Jacob — most configs can be added in minutes |

---

## Pro tips

- **Run it live on the call.** Share your screen. Watching Tamarack make the destination while Flatwing diverts is more persuasive than any PDF.
- **Use the prospect's actual top-3 routes**, not generic examples. Pull them from JetNet flight history if you have it.
- **Always Compare, never Single.** The delta is the pitch.
- **Save the screenshots** into the prospect's Salesforce record so the next call picks up where this one left off.

---

_Need the full feature reference? Ping Nick — there's a comprehensive engineering guide in the simulator repo._

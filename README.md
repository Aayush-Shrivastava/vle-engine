# VLE Engine

A lightweight, interactive command-line Vapour-Liquid Equilibrium engine built in Python from scratch. Designed for chemical engineers and students who need quick, reliable phase equilibrium calculations without the overhead of a full process simulator.

**Built by:** Aayush Shrivastava, Chemical Engineering, BIT Mesra

---

## What It Does

The engine covers 12 calculation functions across the full VLE workflow:

| # | Function |
|---|----------|
| 1 | Vapour Pressure Calculator (Antoine Equation) |
| 2 | Activity Coefficient Calculator |
| 3 | Bubble Pressure |
| 4 | Bubble Temperature |
| 5 | Dew Pressure |
| 6 | Dew Temperature |
| 7 | Pxy Phase Diagram |
| 8 | Txy Phase Diagram |
| 9 | xy Equilibrium Diagram |
| 10 | Multiple Diagrams (combined plots) |
| 11 | Isothermal Flash |
| 12 | Adiabatic Flash |

Every calculation module supports a **"change one parameter and recalculate"** workflow — vary composition, temperature, pressure, or thermodynamic model without re-entering the full system data.

---

## Thermodynamic Models Supported

|      Model        |              Type               |     Systems    |
|-------------------|---------------------------------|----------------|
| Raoult's Law      | Ideal                           | All            |
| 2-Suffix Margules | Activity coefficient            | Binary         |
| 3-Suffix Margules | Activity coefficient            | Binary         |
| Van Laar          | Activity coefficient            | Binary         |
| Wilson            | Activity coefficient            | Multicomponent |
| NRTL              | Activity coefficient            | Multicomponent |
| UNIQUAC           | Activity coefficient            | Multicomponent |
| UNIFAC            | Predictive (group contribution) | Multicomponent |

UNIFAC uses original Fredenslund/Gmehling (1977/1982) parameters — not the modified Dortmund version. A built-in database covers 50+ petroleum-industry components across alkanes, alkenes, aromatics, oxygenates, sulfur compounds, and light gases.

---

## Numerical Methods

- **Newton-Raphson** — primary solver for all bubble/dew/flash calculations
- **Bisection Method** — automatic fallback when Newton-Raphson fails to converge
- Convergence tolerance: 1×10⁻⁶
- Maximum iterations: 500

---

## Special Features

- **Azeotrope detection** — automatically detects and marks azeotropic compositions on xy diagrams
- **Full unit support** — temperature (K, °C, °F, °R) and pressure (mmHg, Torr, bar, Pa, kPa, psi, atm) with automatic conversion throughout
- **Both Antoine forms** — log₁₀ and ln forms supported
- **Flash plots** — VF vs T, VF vs P for isothermal flash; Tflash vs P and VF vs P for adiabatic flash with phase boundary markers
- **Modular architecture** — each calculation module is independently importable
- **Phase boundary markers** — bubble and dew pressure/temperature marked on all flash plots

---

## Project Structure

```
vle-engine/
├── README.md
├── VALIDATION.md
├── requirements.txt
├── vle_engine.py
├── activity_coefficients_models.py
├── antoine.py
├── bubble_pressure.py
├── bubble_temperature.py
├── dew_pressure.py
├── dew_temperature.py
├── flash_calculator.py
├── gamma_calculator.py
├── input_helper.py
├── model_selector.py
├── numericalmethods.py
├── plot.py
├── pressureconversion.py
└── unifac_data.py

---

## Requirements

```
Python 3.8+
matplotlib

```

Install dependencies:
```bash
pip install matplotlib 
```

---

## How to Run

```bash
git clone https://github.com/yourusername/vle-engine.git
cd vle-engine/vle_engine
python vle_engine.py
```

---

## Example: Bubble Pressure, Benzene-Toluene

**System:** Benzene (1) / Toluene (2), equimolar liquid, 80°C, Raoult's Law

**Antoine coefficients (mmHg, °C):**
- Benzene: A=6.90565, B=1211.033, C=220.790
- Toluene: A=6.95464, B=1344.800, C=219.482

**Result:**
```
Bubble Pressure : 530.1 mmHg | 70.68 kPa
y1 (Benzene)    : 0.7170
y2 (Toluene)    : 0.2830
```

Manual verification: P = 0.5×760 + 0.5×300.2 = 530.1 mmHg ✓

---

## Example: Azeotrope Detection, Ethanol-Water

**System:** Ethanol (1) / Water (2), Wilson model, 101.325 kPa

Known azeotrope at x₁ ≈ 0.894, T ≈ 78.15°C

The engine automatically detects and marks this on the xy diagram.

---

## Example: Isothermal Flash, Benzene-Toluene

**System:** Benzene (1) / Toluene (2), z₁=0.5, T=80°C, P=500 mmHg, Ideal

```
Phase State     : Two Phase
Vapour Fraction : 0.3521
x₁ (Benzene)    : 0.4129
y₁ (Benzene)    : 0.6293
Bubble Pressure : 530.1 mmHg
Dew Pressure    : 456.2 mmHg
```

---

## Scope and Limitations

- Non-ideal activity coefficient models (Margules, Van Laar) are implemented for binary systems only. Wilson, NRTL, UNIQUAC, and UNIFAC support multicomponent systems.
- Adiabatic flash assumes temperature-independent Cp and Hvap. This introduces 2-5% error over narrow temperature ranges which is acceptable for preliminary engineering calculations.
- Adiabatic flash unit conversion is fully supported for J/mol and kJ/mol basis. Mass-based units require molecular weight input which is planned for a future update.
- No liquid-liquid equilibrium (LLE) — planned for future scope.
- UNIFAC database covers petroleum and common chemical industry components. Exotic molecules may need to be added manually to `unifac_data.py`.

---

## Validation

A full validation suite was run against analytical solutions, pure component 
limits, and literature reference values before publication.

19 numerical test cases were executed covering all 12 functions, alongside 
4 graphical validation checklists. All tests passed within accepted engineering 
tolerances.

Full test cases, inputs, expected values, deviations, and pass/fail status are 
documented in [VALIDATION.md](VALIDATION.md).

---

## Scope and Limitations

**Activity Coefficient Models:**
- 2-Suffix Margules, 3-Suffix Margules, and Van Laar are implemented for binary systems only. Wilson, NRTL, UNIQUAC, and UNIFAC support multicomponent systems.
- Model parameters must be supplied by the user — the engine does not perform parameter regression from experimental data.

**UNIFAC:**
- The built-in database covers ~50 petroleum and common chemical industry components. Exotic or specialty molecules may not be available and would need to be added manually to `unifac_data.py`.
- Uses original Fredenslund/Gmehling (1977/1982) parameters only. Modified UNIFAC (Dortmund) is not implemented.
- Group interaction parameters for some uncommon pairs default to 0.0 due to limited literature data.

**Adiabatic Flash:**
- Cp (liquid and vapour) and heat of vaporisation (Hvap) are treated as temperature-independent constants. This introduces approximately 2-5% error over narrow temperature ranges, which is acceptable for preliminary engineering calculations but not for high-accuracy design work.
- Unit conversion for enthalpy data supports J/mol and kJ/mol only. Mass-based units (J/kg, kJ/kg) require molecular weight which would need a separate component database — planned for a future update.
- The adiabatic flash solver scans downward from feed temperature in 0.5K steps to find the energy balance bracket. For systems with very sharp energy balance transitions this may occasionally miss the bracket — the bisection fallback handles most such cases.
- All-liquid adiabatic flash requires feed temperatures near or below the bubble point at flash conditions.

**Flash Calculations General:**
- Non-ideal multicomponent flash (3+ components) with activity coefficient models is supported for Wilson, NRTL, UNIQUAC, and UNIFAC only. Margules and Van Laar are restricted to binary flash.
- No liquid-liquid equilibrium (LLE) or three-phase flash — planned for future scope.

**Plots:**
- VF vs T plot requires Antoine equation data to be entered. It is not available when vapour pressures are entered manually since Psat must be recalculated at each temperature step.
- Adiabatic flash plots similarly require Antoine data for the pressure sweep.

**General:**
- The engine is interactive command-line only. No GUI or web interface currently exists — planned as a future development.
- All calculations assume vapour phase ideality (fugacity coefficients = 1). This is valid at low to moderate pressures but breaks down at high pressures where an equation of state would be needed.
- No built-in Antoine coefficient database — coefficients must be entered manually by the user each session.

---

## Future Development

The current limitations outlined above are acknowledged and will be progressively addressed in future versions. Planned improvements include expanding the UNIFAC database, adding molecular weight support for mass-based enthalpy units in adiabatic flash, implementing multicomponent Margules and Van Laar for completeness, adding LLE capability, and eventually a web-based interface to make the engine accessible without a Python installation.

---

## License

MIT License. Free to use, modify, and distribute with attribution.

---

## Author

**Aayush Shrivastava**
Chemical Engineering, BIT Mesra, Ranchi
[LinkedIn](http://linkedin.com/in/aayush-shrivastava-a5568b346)
[GitHub](https://github.com/Aayush-Shrivastava/vle-engine/tree/master)

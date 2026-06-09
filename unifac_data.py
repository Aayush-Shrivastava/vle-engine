# =============================================================================
# UNIFAC DATABASE
# Sources: Fredenslund et al. (1977), Gmehling et al. (1982),
#          Poling, Prausnitz & O'Connell - Properties of Gases and Liquids 5th Ed.
# =============================================================================

UNIFAC_COMPONENTS = {

    # --- ALKANES ---
    "methane": {
        "r": 1.1244,
        "q": 1.1240,
        "groups": {"CH4": 1}
    },
    "ethane": {
        "r": 1.8480,
        "q": 1.6960,
        "groups": {"CH3": 2}
    },
    "propane": {
        "r": 2.5220,
        "q": 2.2360,
        "groups": {"CH3": 2, "CH2": 1}
    },
    "n-butane": {
        "r": 3.1960,
        "q": 2.7760,
        "groups": {"CH3": 2, "CH2": 2}
    },
    "n-pentane": {
        "r": 3.8700,
        "q": 3.3160,
        "groups": {"CH3": 2, "CH2": 3}
    },
    "n-hexane": {
        "r": 4.5440,
        "q": 3.8560,
        "groups": {"CH3": 2, "CH2": 4}
    },
    "n-heptane": {
        "r": 5.2180,
        "q": 4.3960,
        "groups": {"CH3": 2, "CH2": 5}
    },
    "n-octane": {
        "r": 5.8920,
        "q": 4.9360,
        "groups": {"CH3": 2, "CH2": 6}
    },
    "n-nonane": {
        "r": 6.5660,
        "q": 5.4760,
        "groups": {"CH3": 2, "CH2": 7}
    },
    "n-decane": {
        "r": 7.2400,
        "q": 6.0160,
        "groups": {"CH3": 2, "CH2": 8}
    },
    "isobutane": {
        "r": 3.1960,
        "q": 2.7760,
        "groups": {"CH3": 3, "CH": 1}
    },
    "isopentane": {
        "r": 3.8700,
        "q": 3.3160,
        "groups": {"CH3": 3, "CH2": 1, "CH": 1}
    },
    "2-methylpentane": {
        "r": 4.5440,
        "q": 3.8560,
        "groups": {"CH3": 3, "CH2": 2, "CH": 1}
    },
    "2,2-dimethylbutane": {
        "r": 4.5440,
        "q": 3.8560,
        "groups": {"CH3": 4, "CH2": 1, "C": 1}
    },
    "2,3-dimethylbutane": {
        "r": 4.5440,
        "q": 3.8560,
        "groups": {"CH3": 4, "CH": 2}
    },
    "cyclohexane": {
        "r": 4.0460,
        "q": 3.2400,
        "groups": {"CH2cyc": 6}
    },
    "methylcyclohexane": {
        "r": 4.7200,
        "q": 3.7760,
        "groups": {"CH3": 1, "CH2cyc": 5, "CHcyc": 1}
    },

    # --- ALKENES ---
    "ethylene": {
        "r": 1.5440,
        "q": 1.4760,
        "groups": {"CH2=CH2": 1}
    },
    "propylene": {
        "r": 2.2180,
        "q": 2.0160,
        "groups": {"CH3": 1, "CH2=CH": 1}
    },
    "1-butene": {
        "r": 2.8920,
        "q": 2.5560,
        "groups": {"CH3": 1, "CH2": 1, "CH2=CH": 1}
    },
    "1-pentene": {
        "r": 3.5660,
        "q": 3.0960,
        "groups": {"CH3": 1, "CH2": 2, "CH2=CH": 1}
    },
    "1-hexene": {
        "r": 4.2400,
        "q": 3.6360,
        "groups": {"CH3": 1, "CH2": 3, "CH2=CH": 1}
    },
    "2-butene": {
        "r": 2.8920,
        "q": 2.5560,
        "groups": {"CH3": 2, "CH=CH": 1}
    },
    "isobutylene": {
        "r": 2.8920,
        "q": 2.5560,
        "groups": {"CH3": 2, "CH2=C": 1}
    },
    "1,3-butadiene": {
        "r": 2.2180,
        "q": 2.0160,
        "groups": {"CH2=CH": 2}
    },

    # --- AROMATICS ---
    "benzene": {
        "r": 3.1878,
        "q": 2.4000,
        "groups": {"ACH": 6}
    },
    "toluene": {
        "r": 3.9228,
        "q": 2.9680,
        "groups": {"ACH": 5, "ACCH3": 1}
    },
    "ethylbenzene": {
        "r": 4.6000,
        "q": 3.5080,
        "groups": {"ACH": 5, "ACCH2": 1, "CH3": 1}
    },
    "o-xylene": {
        "r": 4.6578,
        "q": 3.5360,
        "groups": {"ACH": 4, "ACCH3": 2}
    },
    "m-xylene": {
        "r": 4.6578,
        "q": 3.5360,
        "groups": {"ACH": 4, "ACCH3": 2}
    },
    "p-xylene": {
        "r": 4.6578,
        "q": 3.5360,
        "groups": {"ACH": 4, "ACCH3": 2}
    },
    "styrene": {
        "r": 4.4000,
        "q": 3.3000,
        "groups": {"ACH": 5, "AC": 1, "CH2=CH": 1}
    },
    "naphthalene": {
        "r": 5.2420,
        "q": 3.9840,
        "groups": {"ACH": 8, "AC": 2}
    },
    "cumene": {
        "r": 5.2740,
        "q": 4.0480,
        "groups": {"ACH": 5, "ACCH": 1, "CH3": 2}
    },

    # --- OXYGENATES ---
    "methanol": {
        "r": 1.4311,
        "q": 1.4320,
        "groups": {"CH3OH": 1}
    },
    "ethanol": {
        "r": 2.1055,
        "q": 1.9720,
        "groups": {"CH3": 1, "CH2": 1, "OH": 1}
    },
    "1-propanol": {
        "r": 2.7795,
        "q": 2.5120,
        "groups": {"CH3": 1, "CH2": 2, "OH": 1}
    },
    "2-propanol": {
        "r": 2.7795,
        "q": 2.5080,
        "groups": {"CH3": 2, "CH": 1, "OH": 1}
    },
    "1-butanol": {
        "r": 3.4535,
        "q": 3.0520,
        "groups": {"CH3": 1, "CH2": 3, "OH": 1}
    },
    "2-butanol": {
        "r": 3.4535,
        "q": 3.0480,
        "groups": {"CH3": 2, "CH2": 1, "CH": 1, "OH": 1}
    },
    "tert-butanol": {
        "r": 3.4535,
        "q": 3.0440,
        "groups": {"CH3": 3, "C": 1, "OH": 1}
    },
    "acetone": {
        "r": 2.5740,
        "q": 2.3360,
        "groups": {"CH3": 2, "CH3CO": 1}
    },
    "methyl-ethyl-ketone": {
        "r": 3.2480,
        "q": 2.8760,
        "groups": {"CH3": 1, "CH2": 1, "CH3CO": 1}
    },
    "diethyl-ether": {
        "r": 3.5160,
        "q": 3.1440,
        "groups": {"CH3": 2, "CH2": 2, "CH2O": 1}
    },
    "methyl-tert-butyl-ether": {
        "r": 4.0678,
        "q": 3.6320,
        "groups": {"CH3": 3, "C": 1, "CH3O": 1}
    },
    "acetic-acid": {
        "r": 2.2024,
        "q": 2.0720,
        "groups": {"CH3": 1, "COOH": 1}
    },
    "formic-acid": {
        "r": 1.5280,
        "q": 1.5320,
        "groups": {"HCOOH": 1}
    },
    "ethyl-acetate": {
        "r": 3.4786,
        "q": 3.1160,
        "groups": {"CH3": 2, "CH2": 1, "CH3COO": 1}
    },
    "dimethyl-sulfoxide": {
        "r": 2.8266,
        "q": 2.4720,
        "groups": {"CH3": 2, "DMSO": 1}
    },

    # --- NITROGEN COMPOUNDS ---
    "acetonitrile": {
        "r": 1.8701,
        "q": 1.7240,
        "groups": {"CH3CN": 1}
    },
    "aniline": {
        "r": 3.7200,
        "q": 2.8320,
        "groups": {"ACH": 5, "ACNH2": 1}
    },

    # --- CHLORINATED ---
    "chloroform": {
        "r": 2.8700,
        "q": 2.4100,
        "groups": {"CHCl3": 1}
    },
    "carbon-tetrachloride": {
        "r": 3.3900,
        "q": 2.9100,
        "groups": {"CCl4": 1}
    },
    "dichloromethane": {
        "r": 2.2564,
        "q": 1.9880,
        "groups": {"CH2Cl2": 1}
    },

    # --- INORGANICS / LIGHT GASES ---
    "water": {
        "r": 0.9200,
        "q": 1.4000,
        "groups": {"H2O": 1}
    },
    "hydrogen-sulfide": {
        "r": 1.2350,
        "q": 1.2020,
        "groups": {"H2S": 1}
    },
    "carbon-dioxide": {
        "r": 1.3000,
        "q": 1.1200,
        "groups": {"CO2": 1}
    },

    # --- SULFUR COMPOUNDS (petroleum) ---
    "dimethyl-sulfide": {
        "r": 2.5680,
        "q": 2.3320,
        "groups": {"CH3": 2, "CH3S": 1}
    },
    "thiophene": {
        "r": 2.8569,
        "q": 2.1400,
        "groups": {"ACH": 4, "ACS": 1}
    },

    # --- GLYCOLS (refinery/gas processing) ---
    "ethylene-glycol": {
        "r": 2.4088,
        "q": 2.2480,
        "groups": {"CH2": 2, "OH": 2}
    },
    "diethylene-glycol": {
        "r": 3.9540,
        "q": 3.5960,
        "groups": {"CH2": 4, "OH": 2, "CH2O": 1}
    },
}


GROUP_RQ = {
    # Paraffin groups
    "CH3":      {"R": 0.9011, "Q": 0.8480},
    "CH2":      {"R": 0.6744, "Q": 0.5400},
    "CH":       {"R": 0.4469, "Q": 0.2280},
    "C":        {"R": 0.2195, "Q": 0.0000},
    "CH4":      {"R": 1.1244, "Q": 1.1240},  

    # Cyclic paraffin groups
    "CH2cyc":   {"R": 0.6744, "Q": 0.5400},
    "CHcyc":    {"R": 0.4469, "Q": 0.2280},

    # Olefin groups
    "CH2=CH2":  {"R": 1.5440, "Q": 1.4760},  
    "CH2=CH":   {"R": 1.3454, "Q": 1.1760},
    "CH=CH":    {"R": 1.1167, "Q": 0.8670},
    "CH2=C":    {"R": 1.1173, "Q": 0.9880},
    "CH=C":     {"R": 0.8886, "Q": 0.6760},

    # Aromatic groups
    "ACH":      {"R": 0.5313, "Q": 0.4000},
    "AC":       {"R": 0.3652, "Q": 0.1200},
    "ACCH3":    {"R": 1.2663, "Q": 0.9680},
    "ACCH2":    {"R": 1.0396, "Q": 0.6600},
    "ACCH":     {"R": 0.8121, "Q": 0.3480},
    "ACS":      {"R": 0.4000, "Q": 0.2200},  

    # Hydroxyl groups
    "OH":       {"R": 1.0000, "Q": 1.2000},
    "CH3OH":    {"R": 1.4311, "Q": 1.4320},  

    # Water
    "H2O":      {"R": 0.9200, "Q": 1.4000},

    # Carbonyl / ether groups
    "CH3CO":    {"R": 1.6724, "Q": 1.4880},
    "CH2CO":    {"R": 1.4457, "Q": 1.1800},
    "CHO":      {"R": 0.9980, "Q": 0.9480},   
    "CH3COO":   {"R": 1.9031, "Q": 1.7280},  
    "CH2COO":   {"R": 1.6764, "Q": 1.4200},
    "HCOO":     {"R": 1.2420, "Q": 1.1880},  
    "CH3O":     {"R": 1.1450, "Q": 1.0880},  
    "CH2O":     {"R": 0.9183, "Q": 0.7800},  
    "CHO_eth":  {"R": 0.6908, "Q": 0.4680},  

    # Acid groups
    "COOH":     {"R": 1.3013, "Q": 1.2240},
    "HCOOH":    {"R": 1.5280, "Q": 1.5320},  

    # Nitrogen groups
    "CH3CN":    {"R": 1.8701, "Q": 1.7240},  
    "ACNH2":    {"R": 1.0600, "Q": 0.8160},  

    # Chlorinated groups
    "CHCl3":    {"R": 2.8700, "Q": 2.4100},
    "CCl4":     {"R": 3.3900, "Q": 2.9100},
    "CH2Cl2":   {"R": 2.2564, "Q": 1.9880},
    "CHCl2":    {"R": 1.8000, "Q": 1.5480},
    "CHCl":     {"R": 1.4654, "Q": 1.2640},
    "CCl3":     {"R": 2.6401, "Q": 2.1840},
    "CCl2":     {"R": 2.2940, "Q": 1.8160},

    # Sulfur groups
    "CH3S":     {"R": 1.6130, "Q": 1.3680},
    "CH2S":     {"R": 1.3863, "Q": 1.0600},
    "DMSO":     {"R": 2.8266, "Q": 2.4720},  
    # Light gases
    "H2S":      {"R": 1.2350, "Q": 1.2020},
    "CO2":      {"R": 1.3000, "Q": 1.1200},
}



GROUP_INTERACTIONS = {

    "CH3": {
        "CH2":      0.0,
        "CH":       0.0,
        "C":        0.0,
        "CH2cyc":   0.0,
        "CHcyc":    0.0,
        "CH2=CH":   -35.36,
        "CH=CH":    -35.36,
        "CH2=C":    -35.36,
        "ACH":      61.13,
        "AC":       61.13,
        "ACCH3":    76.50,
        "ACCH2":    76.50,
        "OH":       986.5,
        "CH3OH":    697.2,
        "H2O":      1318.0,
        "CH3CO":    476.4,
        "CH2CO":    476.4,
        "COOH":     663.5,
        "CH3COO":   232.1,
        "CH2O":     251.5,
        "CH3O":     251.5,
        "CH3CN":    597.0,
        "CHCl3":    35.93,
        "CCl4":     -78.45,
        "CH2Cl2":   53.76,
        "CH3S":     52.10,
        "H2S":      692.7,
        "CO2":      725.0,
    },

    "CH2": {
        "CH3":      0.0,
        "CH":       0.0,
        "C":        0.0,
        "CH2cyc":   0.0,
        "CHcyc":    0.0,
        "CH2=CH":   -35.36,
        "ACH":      61.13,
        "ACCH3":    76.50,
        "OH":       986.5,
        "CH3OH":    697.2,
        "H2O":      1318.0,
        "CH3CO":    476.4,
        "COOH":     663.5,
        "CH3COO":   232.1,
        "CH2O":     251.5,
        "CH3O":     251.5,
        "CH3CN":    597.0,
        "CHCl3":    35.93,
        "CCl4":     -78.45,
        "CH3S":     52.10,
        "H2S":      692.7,
        "CO2":      725.0,
    },

    "CH2cyc": {
        "CH3":      0.0,
        "CH2":      0.0,
        "ACH":      61.13,
        "OH":       986.5,
        "H2O":      1318.0,
        "CH3CO":    476.4,
        "CH3CN":    597.0,
    },

    "CH2=CH": {
        "CH3":      86.02,
        "CH2":      86.02,
        "ACH":      -114.0,
        "OH":       693.0,
        "H2O":      862.1,
        "CH3CO":    526.1,
    },

    "ACH": {
        "CH3":      -11.12,
        "CH2":      -11.12,
        "CH":       -11.12,
        "CH2=CH":   -114.0,
        "ACH":      0.0,
        "AC":       0.0,
        "ACCH3":    167.0,
        "ACCH2":    167.0,
        "OH":       636.1,
        "CH3OH":    637.4,
        "H2O":      903.8,
        "CH3CO":    25.77,
        "COOH":     537.4,
        "CH3COO":   5.994,
        "CH2O":     32.14,
        "CH3O":     32.14,
        "CH3CN":    212.5,
        "CHCl3":    -146.8,
        "CCl4":     -114.1,
        "CH2Cl2":   -141.4,
        "CH3S":     -60.71,
        "H2S":      261.5,
        "CO2":      0.0,
    },

    "ACCH3": {
        "CH3":      -69.70,
        "CH2":      -69.70,
        "ACH":      -146.8,
        "OH":       803.2,
        "H2O":      5695.0,
        "CH3CO":    -52.10,
        "COOH":     603.3,
        "CH3COO":   -7.838,
        "CH3CN":    6.712,
    },

    "ACCH2": {
        "CH3":      -69.70,
        "CH2":      -69.70,
        "ACH":      -146.8,
        "OH":       803.2,
        "H2O":      5695.0,
        "CH3CO":    -52.10,
    },

    "OH": {
        "CH3":      156.4,
        "CH2":      156.4,
        "CH":       156.4,
        "CH2cyc":   156.4,
        "ACH":      89.60,
        "ACCH3":    75.62,
        "OH":       0.0,
        "CH3OH":    -137.1,
        "H2O":      -229.1,
        "CH3CO":    164.5,
        "COOH":     199.0,
        "CH3COO":   101.1,
        "CH2O":     28.06,
        "CH3O":     28.06,
        "CH3CN":    6.712,
        "CHCl3":    -229.0,
        "CH3S":     112.6,
        "H2S":      -24.36,
    },

    "CH3OH": {
        "CH3":      16.51,
        "CH2":      16.51,
        "ACH":      -50.00,
        "OH":       249.1,
        "H2O":      -181.0,
        "CH3CO":    23.39,
        "COOH":     -202.0,
        "CH3COO":   -10.72,
        "CH2O":     -128.6,
        "CH3CN":    -15.05,
        "CHCl3":    -139.4,
        "CCl4":     -119.8,
    },

    "H2O": {
        "CH3":      300.0,
        "CH2":      300.0,
        "CH2cyc":   300.0,
        "ACH":      362.3,
        "ACCH3":    377.6,
        "OH":       289.6,
        "CH3OH":    242.8,
        "H2O":      0.0,
        "CH3CO":    472.5,
        "COOH":     -14.09,
        "CH3COO":   72.87,
        "CH2O":     540.5,
        "CH3O":     540.5,
        "CH3CN":    -14.05,
        "CHCl3":    -23.25,
        "CH3S":     399.5,
        "H2S":      -23.71,
        "CO2":      -59.24,
    },

    "CH3CO": {
        "CH3":      26.76,
        "CH2":      26.76,
        "ACH":      140.1,
        "ACCH3":    365.8,
        "OH":       -84.00,
        "CH3OH":    128.0,
        "H2O":      472.5,
        "CH3CO":    0.0,
        "COOH":     669.4,
        "CH3COO":   -213.7,
        "CH2O":     -103.6,
        "CH3CN":    -103.6,
        "CHCl3":    -182.2,
        "CCl4":     -47.51,
    },

    "COOH": {
        "CH3":      315.3,
        "CH2":      315.3,
        "ACH":      62.32,
        "ACCH3":    89.86,
        "OH":       -151.0,
        "CH3OH":    -66.17,
        "H2O":      -14.09,
        "CH3CO":    -297.8,
        "COOH":     0.0,
        "CH3COO":   -256.3,
        "CH2O":     -235.7,
        "CH3CN":    -256.3,
    },

    "CH3COO": {
        "CH3":      114.8,
        "CH2":      114.8,
        "ACH":      85.84,
        "ACCH3":    -170.0,
        "OH":       245.4,
        "CH3OH":    249.6,
        "H2O":      200.8,
        "CH3CO":    372.2,
        "COOH":     660.2,
        "CH3COO":   0.0,
        "CH2O":     -235.7,
        "CH3CN":    -95.00,
        "CHCl3":    -257.0,
    },

    "CH2O": {
        "CH3":      83.36,
        "CH2":      83.36,
        "ACH":      52.13,
        "OH":       237.7,
        "CH3OH":    238.4,
        "H2O":      -314.7,
        "CH3CO":    191.1,
        "COOH":     664.6,
        "CH3COO":   337.1,
        "CH2O":     0.0,
        "CH3CN":    -7.838,
        "CHCl3":    -66.46,
    },

    "CH3O": {
        "CH3":      83.36,
        "CH2":      83.36,
        "ACH":      52.13,
        "OH":       237.7,
        "CH3OH":    238.4,
        "H2O":      -314.7,
        "CH3CO":    191.1,
        "CH2O":     0.0,
        "CH3CN":    -7.838,
    },

    "CH3CN": {
        "CH3":      -121.3,
        "CH2":      -121.3,
        "ACH":      -49.29,
        "ACCH3":    -49.29,
        "OH":       353.5,
        "CH3OH":    75.14,
        "H2O":      270.6,
        "CH3CO":    362.3,
        "COOH":     492.0,
        "CH3COO":   534.7,
        "CH2O":     112.6,
        "CH3CN":    0.0,
        "CHCl3":    -47.25,
    },

    "CHCl3": {
        "CH3":      -64.13,
        "CH2":      -64.13,
        "ACH":      -146.8,
        "OH":       -259.7,
        "CH3OH":    -246.0,
        "H2O":      561.6,
        "CH3CO":    -195.4,
        "CH3COO":   -338.5,
        "CH2O":     -234.0,
        "CH3CN":    -195.4,
        "CHCl3":    0.0,
        "CCl4":     -9.451,
    },

    "CCl4": {
        "CH3":      -7.680,
        "CH2":      -7.680,
        "ACH":      -106.3,
        "OH":       -64.38,
        "CH3OH":    -84.52,
        "H2O":      600.0,
        "CH3CO":    -7.838,
        "CH3COO":   -103.6,
        "CHCl3":    -9.451,
        "CCl4":     0.0,
    },

    "CH2Cl2": {
        "CH3":      -111.0,
        "CH2":      -111.0,
        "ACH":      -107.6,
        "OH":       -52.39,
        "CH3OH":    -73.08,
        "H2O":      529.0,
        "CH3CO":    -26.06,
        "CH2Cl2":   0.0,
    },

    "CH3S": {
        "CH3":      -18.91,
        "CH2":      -18.91,
        "ACH":      -49.29,
        "OH":       -64.38,
        "H2O":      -68.93,
        "CH3S":     0.0,
    },

    "H2S": {
        "CH3":      -53.91,
        "CH2":      -53.91,
        "ACH":      -80.25,
        "OH":       -192.0,
        "H2O":      -147.3,
        "H2S":      0.0,
        "CO2":      46.40,
    },

    "CO2": {
        "CH3":      -38.90,
        "CH2":      -38.90,
        "ACH":      -38.90,
        "H2O":      149.9,
        "H2S":      46.40,
        "CO2":      0.0,
    },

    "ACNH2": {
        "CH3":      -23.51,
        "CH2":      -23.51,
        "ACH":      -23.51,
        "OH":       -119.2,
        "H2O":      -41.11,
        "ACNH2":    0.0,
    },

    "HCOOH": {
        "CH3":      315.3,
        "CH2":      315.3,
        "ACH":      62.32,
        "OH":       -151.0,
        "H2O":      -14.09,
        "HCOOH":    0.0,
    },
}


def get_interaction(group_m, group_n):
    """
    Returns UNIFAC interaction parameter a_mn (in Kelvin).
    Returns 0.0 if groups are identical or pair is not in the table.
    """
    if group_m == group_n:
        return 0.0
    return GROUP_INTERACTIONS.get(group_m, {}).get(group_n, 0.0)
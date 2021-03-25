# # Imports
import fileinput
import re
import os

# ----------------------------------------------------------------------------
# Input Variables

# Replacement pattern must match the pattern in the set file that you are trying to replace
replacementPattern = r'cost [0-9]+'

# This SINGLE string entry is when enables a state Change check
# Vehicle Class Search Pattern in the set file must start and end with comment
commentTrigger = ';'

# List of vehicle properties to update in the set files
# Default: Cost
vehiclePropsTable = {
    # lightmgcar
    "lightmgcar": {
        "bx10_mgun": 110,
        "caiman_m2": 70,
        "car_terror": 60,
        "cobra": 120,
        "datsun-620": 100,
        "dingo": 100,
        "dingo(eu)": 100,
        "eq2050": 100,
        "hmmwv_turret": 120,
        "hummvee": 100,
        "hummvee_m240": 100,
        "iveco_cammo-brow": 110,
        "iveco_cammo-brow(eu)": 110,
        "iveco_cammo-mg": 100,
        "iveco_cammo-mg(eu)": 100,
        "iveco_cammo-mk19": 180,
        "iveco_cammo-mk19(eu)": 180,
        "jeep_cj5_mgun": 80,
        "kubel_mgun": 30,
        "land_rover_sas": 80,
        "landrover109_mgun": 80,
        "landrover109_mgun(fr)": 80,
        "landrover110": 80,
        "m151_mg": 80,
        "nj_2046_mgun": 80,
        "r12": 20,
        "sdkfz251_1": 40,
        "skorpion3": 70,
        "tigr_armenia": 110,
        "tigr_cis": 110,
        "tigr_ukr": 110,
        "toyota_hilux": 60,
        "tumak": 100,
        "tumak_pkm": 100,
        "uaz-469_ags": 150,
        "uaz-469_mg": 80,
        "uaz-469_mg(pol)": 80,
        "uaz-469_mg(rus)": 80,
        "uaz469_mgun": 80,
        "uaz_dchk": 90,
        "vabl": 120,
        "vw183_mg": 80,
        "yongswydaiq": 80,
        "zzc-55": 120
    },

    # heavymgcar
    "heavymgcar": {
        "boragh": 170,
        "brdm1": 120,
        "brdm1(nva)": 120,
        "brdm2": 140,
        "brdm2(ddr)": 140,
        "brdm2(makedonia)": 140,
        "brdm2(nva)": 140,
        "btr-40": 120,
        "btr-40(ddr)": 120,
        "btr-40(nva)": 120,
        "btr-40(pol)": 120,
        "btr-40b_armenia": 120,
        "btr-40b_bel": 120,
        "btr-40b_cis": 120,
        "btr-40b_ukr": 120,
        "btr152": 125,
        "btr50pb": 125,
        "btr50pb(ddr)": 125,
        "btr50pb(nva)": 125,
        # Russian version
        "btr60": 130,
        "btr80": 200,
        "btr80a": 220,
        "btr_70": 190,
        "hummvee_mk19": 150,
        "maxxpro": 150,
        "ridgback_d": 100,
        "vab": 140,
        "vab(eu)": 140,
        "vodnik": 150,
        "zsl56": 125
    },

    # transport
    "transport": {
        "bedfordmt": 50,
        "blitz3_6": 50,
        "bx10": 50,
        "ifa": 50,
        "jelcz442": 50,
        "jelcz662": 50,
        "kamaz-4326": 50,
        "kamaz-6350": 50,
        "kamaz_43118": 50,
        "landrover109_t": 50,
        "landrover109_t(fr)": 50,
        "m151": 50,
        "m35": 50,
        "m939": 50,
        "m939a1": 50,
        "man": 50,
        "man-7t": 50,
        "mtvr": 50,
        "mtvr_mgun": 50,
        "rsx2190": 50,
        "skw45": 50,
        "star266": 50,
        "tarbant": 50,
        "toyota_hilux_transport": 50,
        "ural_zvezda": 50,
        "zil157": 50,
        "zis_151": 50
    },

    # logi
    "logi": {
        "KAMAZ_43118_fuel": 100,
        "bedford_support": 100,
        "bedfordmt_eng": 100,
        "blitz3_6art": 100,
        "blitz3_6eng": 100,
        "ifa_eng": 100,
        "ifa_support": 100,
        "m35_ammo": 100,
        "m35_eng": 100,
        "m939_ammo": 100,
        "m939_eng": 100,
        "m939a1_amo": 100,
        "m939a1_eng": 100,
        "man_amo": 100,
        "man_eng": 100,
        "mtlb": 100,
        "mtlb(pol)": 100,
        "mtlb_amo": 100,
        "mtlb_eng": 100,
        "mtvr_ammo": 100,
        "mtvr_ammo_mgun": 100,
        "mtvr_rem": 100,
        "mtvr_rem_mgun": 100,
        "rsx2190_art": 100,
        "rsx2190_eng": 100,
        "skw45_ammo": 100,
        "skw45_eng": 100,
        "tatra-813": 100,
        "toyota_hilux_ammo": 100,
        "ural-375_ammo": 100,
        "ural-375_eng": 100,
        "ural-375_eng(pol)": 100,
        "ural-4320_ammo": 100,
        "ural-4320_ammo(pol)": 100,
        "ural-4320_ammo(rus)": 100,
        "ural-atz-5-4320_fuel(pol)": 100,
        "zil130_ammo": 100,
        "zil157": 100,
        "zil157_ammo": 100,
        "zil157_eng": 100,
        "zil157_fuel": 100
    },

    # emplacements

    # hmg
    "hmg": {
        "brauning_mini": 70,
        "browning_trenoga": 70,
        "dshk_trenoga": 70,
        "dshkm_mini": 70,
        "dshkm_trenoga": 70,
        "dshkm_trenoga(nva)": 70,
        "fnmag_tstanok(fra)": 60,
        "kord_stan": 70,
        "kpv-44": 110,
        "kpv-44(nva)": 110,
        "m240_tstanok": 60,
        "m240_tstanok(eng)": 60,
        "mg3_tstanok": 60,
        "sgrw42": 40,
        "type85_trenoga": 70
    },

    # minigun
    "minigun": {
        "md134_stan": 90
    },

    # gl
    "gl": {
        "ags30_stan": 80,
        "ags30_stan(nva)": 80,
        "mk19_stan": 80,
        "mk19_stan(eng)": 80,
        "mk19_stan(fra)": 80,
        "qlz04_stan": 80
    },

    # field_artillery
    "field_artillery": {
        "d30": 110,
        "d30a": 115,
        "d30a(nva)": 115,
        "d30a(pol)": 115,
        "l119": 130,
        "ltm1": 190,
        "long_tom": 190,
        "m115": 125,
        "m119": 130,
        "m30_1938": 120,
        "ml20": 120,
        "type-96": 120
    },


    # mortar
    "mortar": {
        "2b14": 70,
        "2b14(nva)": 70,
        "2b14(pol)": 70,
        "l16": 80,
        "l16(fra)": 80,
        "l16(ger)": 80,
        "m252": 80,
        "type_61mortar": 70
    },

    # aa_gun
    "aa_gun": {
        "bofors": 70,
        "china25mmgaopao": 120,
        "flak38_wheeled": 50,
        "type58_aa": 110,
        "zpu_2": 100,
        "zpu_4": 110,
        "zpu_4(nva)": 110,
        "zu_23": 120,
        "zu_23(nva)": 120,
        "zu_23(pol)": 120,
        "zu_artemis30": 150
    },

    # atgm
    "atgm": {
        "ptur_fagot": 100,
        "ptur_metis": 100,
        "ptur_tow": 110,
        "ptur_tow(eng)": 110,
        "ptur_tow(fra)": 110,
        "ptur_tow(ger)": 110,
        "ptur_tow(ita)": 110
    },

    # at_gun
    "at_gun": {
        "mt12_rapira": 70,
        "mt12_rapira(nva)": 70,
        "pak36": 40,
        "pak38": 50,
        "pak40": 60,
        "spg_9": 80,
        "spg_9(nva)": 80,
        "spg_9(pol)": 80,
        "type65_stan": 80,
        "type65_stan(nva)": 80
    },

    # light_mortar_spg
    "light_mortar_spg": {
        "fv432_mortar": 230,
        "m113art": 230,
        "m113art(isr)": 230,
        "m113artg": 230,
        "mtlb_art": 220,
        "mtlb_art(pol)": 220
    },


    # lightspgarty
    "lightspgarty": {
        "2c1_gvazdika": 500,
        "2c1_gvazdika(pol)": 500,
        "2c1_gvazdika(rus)": 500,
        "2c9": 350,
        "2c9(rus)": 350,
        "ahs_ariete_105mm": 600,
        "crusader": 850,
        "dana": 600,
        "fv101_ebbot": 750,
        "lav_rino": 300,
        "m109": 370,
        "m109a1g": 700,
        "m109a2(eng)": 750,
        "m109a2g": 750,
        "m109a3": 800,
        "nona-svk": 280,
        "type70_122": 330,
        "type70_122(nva)": 330,
        "wespe": 150
    },

    # heavyspgarty
    "heavyspgarty": {
        "akatcia": 950,
        "as90": 900,
        "dana": 750,
        "hummel": 300,
        "k9thunder": 900,
        "m109a6": 1000,
        "malka": 1200,
        "msta": 900,
        "pion": 1200,
        "pion(pol)": 1200,
        "pzh2000": 1000,
        "pzl-83": 900,
        "tochom122": 800
    },

    # lightrocketarty
    "lightrocketarty": {
        "lars1": 900,
        "m142": 900,
        "sdkfz4": 350,
        "type63_type70_rocket(nva)": 800,
        "uragan": 1000
    },

    # heavyrocketarty
    "heavyrocketarty": {
        "bm23": 1010,
        "kamaz-tornado-g": 1200,
        "m270": 1200,
        "m270(1)": 1220,
        "m270(eng)": 1200,
        "m270(fra)": 1200,
        "m270mars": 1200,
        "type60": 1000,
        "ural_grad": 1000,
        "ural_grad(geo)": 1000,
        "ural_grad(pol)": 1000,
        "ural_grad(rus)": 1000
    },

    # light_apc
    "light_apc": {
        "brdm1(pol)": 150,
        "brdm2": 160,
        "brdm2(pol)": 160,
        "btr60": 160,
        "btr60(nva)": 160,
        "btr80": 200,
        "btr_70": 190,
        "fav": 230,
        "fv432": 160,
        "fv432_buldog": 160,
        "m113": 160,
        "m113(isr)": 160,
        "m113a3": 170,
        "m113a3(isr)": 170,
        "m113g": 170,
        "mtlb-6mb": 180,
        "namer": 200,
        "puma": 85,
        "pz1": 100,
        "pz1b": 60,
        "pz2l": 140,
        "sdkfz222": 120,
        "sdkfz223": 80,
        "sdkfz234": 160,
        "stryker_browning": 200,
        "topas": 160,
        "topas-2ap": 170,
        "tpz1a4": 160,
        "tpz1a6": 180,
        "type34": 250,
        "type63": 150,
        "type63(nva)": 150,
        "type63_zsd-90": 210,
        "type63c": 160,
        "type63c(nva)": 160,
        "vtt320": 120,
        "zbik-a": 150
    },

    # medium_wheeled_apc
    "medium_wheeled_apc": {
        "Freccia": 280,
        "VBCI": 280,
        "VBCI(eu)": 280,
        "btr80a": 240,
        "btr_90": 380,
        "btr_90b": 390,
        "btr_90r": 390,
        "lav25a": 300,
        "lav_25": 380,
        "ot64": 220,
        "ot_54": 370,
        "rosomak": 200,
        "sppz2luchs": 210,
        "type89_ifv": 360,
        "type96": 300,
        "wz551": 250,
        "zbd97": 390,
        "zbl-09": 345
    },


    # heavy_apc
    "heavy_apc": {
        "bmd1": 360,
        "bmd1p": 370,
        "bmd1p(rus)": 370,
        "bmd2": 390,
        "bmd2(rus)": 390,
        "bmd_3": 420,
        "bmp1": 350,
        "bmp1(ddr)": 350,
        "bmp1(pol)": 350,
        "bmp1a1": 360,
        "bmp1p": 360,
        "bmp1p(ddr)": 360,
        "bmp1p(pol)": 360,
        "bmp1p(rus)": 360,
        "bmp2": 390,
        "bmp2(ddr)": 390,
        "bmp2(geo)": 390,
        "bmp2(pol)": 390,
        "bmp2(rus)": 390,
        "bmp2m": 400,
        "bmp3": 420,
        "bmp_3": 420,
        "bmp_3m": 420,
        "bmpt1": 500,
        "bmpt2": 500,
        "fv510": 400,
        "ifv-6a": 410,
        "k200": 410,
        "m2a1": 400,
        "m2a2": 410,
        "m2a3": 420,
        "m551": 410,
        "m67": 390,
        "marder1a3": 400,
        "marder1a5": 410,
        "marder1a5(eu)": 410,
        "marder_t": 420,
        "ostwind": 220,
        "ot_54": 370,
        "pz3m": 240,
        "to_55a": 400,
        "warior": 400,
        "warlord": 420,
        "welberwind": 180,
        "wz501": 350,
        "wz501-1": 370,
        "wz501g": 360
    },

    # spg_aa
    "spg_aa": {
        "Gepard1A2": 330,
        "Gepard1A2(eu)": 330,
        "amx-30moskito": 450,
        "bmp_zu23": 290,
        "bmp_zu23(pol)": 290,
        "bmp_zu23(rus)": 290,
        "btr-3d": 300,
        "frp_roland": 300,
        "frr_roland": 300,
        "kamaz_zu": 220,
        "m1097_avenger": 300,
        "m163": 290,
        "m163a1": 295,
        "m163machbet": 310,
        "m2_len": 300,
        "mtlb_zu": 260,
        "mtlb_zu(pol)": 260,
        "mtlb_zu(rus)": 260,
        "pgz-80": 310,
        "sa13": 300,
        "tunguska": 370,
        "type_95_aa": 300,
        "vtt323": 280,
        "wiesel_aa": 300,
        "yongswygaopao": 200,
        "zsu-57-2": 310,
        "zsushilka": 300,
        "zsushilka(nva)": 300,
        "zsushilka(pol)": 300,
        "zsushilka3": 325
    },

    # medium_tank
    "medium_tank": {
        "M48c": 370,
        "amx-30(bos)": 400,
        "centurion_mk10": 425,
        "centurion_mk7": 400,
        "centurion_mk7_shot": 400,
        "china59-1": 410,
        "fv101-90": 300,
        "leopard1": 390,
        "leopard1a1": 400,
        "leopard1a3": 410,
        "leopard1a4": 425,
        "leopard1a5": 450,
        "m48a1": 390,
        "m60a4": 470,
        "ot_54(ddr)": 370,
        "pl01": 400,
        "pz3": 140,
        "pz3f": 120,
        "pz3n": 160,
        "pz4g": 180,
        "pz4h": 200,
        "pz5g": 240,
        "pz6bh": 300,
        "pz6e": 260,
        "st_b1": 470,
        "t_54-3": 370,
        "t_54a": 350,
        "t_54a(ddr)": 390,
        "t_54b": 370,
        "t_55a": 400,
        "t_55a(ddr)": 400,
        "t_55a(pol)": 400,
        "t_55am": 410,
        "t_55mb": 450,
        "t_55mbt": 470,
        "t_62a": 420,
        "t_62a_pks": 450,
        "t_62m": 450,
        "t_62mbt": 470,
        "t_64a": 470,
        "t_64b": 490,
        "t_64bv": 500,
        "t_72a(rus)": 500,
        "t_72b(rus)": 525,
        "t_72b_rogatka": 650,
        "t_72ba": 625,
        "t_80bv(rus)": 700,
        "ti67": 470,
        "type62": 350,
        "type62(nva)": 350,
        "type62b": 390,
        "type_61": 390
    },

    # cold_war_tank
    "cold_war_tank": {
        "amx-30": 400,
        "amx-30b2brenus": 550,
        "chiftein": 440,
        "chiftein2": 430,
        "chiftein_d": 460,
        "china59-1": 410,
        "china59-1(nva)": 410,
        "china59d": 450,
        "china59jaguar": 470,
        "chonmaho4": 525,
        "kzpf70": 600,
        "leopard1a4": 425,
        "leopard1a5": 400,
        "m60a1": 420,
        "m60a2": 430,
        "m60a4": 500,
        "m60m6": 470,
        "m_84(bosnia)": 500,
        "m_84(serbia)": 500,
        "magach7c_gimel": 520,
        "mbt70": 600,
        "songun915": 550,
        "t_62a": 420,
        "t_62a(ddr)": 420,
        "t_62a_pks": 450,
        "t_62m": 450,
        "t_62mbt": 470,
        "t_62mbt(ddr)": 470,
        "t_72a": 500,
        "t_72a(armenia)": 500,
        "t_72a(geo)": 500,
        "t_72b": 525,
        "t_72b(armenia)": 525,
        "t_72b(ddr)": 525,
        "t_72b(geo)": 600,
        "t_72b(makedonia)": 600,
        "t_72m": 500,
        "t_72m(ddr)": 500,
        "t_72m(makedonia)": 500,
        "to_62a": 390
    },

    # heavy_cold_war_tank
    "heavy_cold_war_tank": {
        "leoparda2a4": 550,
        "leoparda2a4(pol)": 550,
        "m1": 540,
        "m1a1": 550,
        "m1a1a": 550,
        "m1a1m": 550,
        "t_64a": 470,
        "t_64bv": 500,
        "t_64bv_tral": 520,
        "t_72b": 525,
        "t_72m": 500,
        "t_72m(pol)": 500,
        "t_80bvkl": 700
    },

    # heavy_modern_war_tank
    "heavy_modern_war_tank": {
        "amx-56": 800,
        "amx-56(eu)": 800,
        "arietemk2": 700,
        "c1_ariete": 650,
        "china99": 710,
        "china99g": 760,
        "k1a1": 750,
        "leoparda2a4": 550,
        "m1a2": 700,
        "m1a2_kom": 750,
        "t_64bm": 700,
        "t_80bv(rus)": 700,
        "t_90": 900,
        "t_90_tral": 550,
        "t_90a": 920,
        "t_90ms": 1000,
        "type_90": 700
    },

    # very_heavy_modern_war_tank
    "very_heavy_modern_war_tank": {
        "challenger": 540,
        "challenger2": 900,
        "challenger2_applique": 910,
        "k2bpanter": 900,
        "m1a2_sel": 1000,
        "m1a2_tusk": 950,
        "merkava_mk4": 900
    },

    # tank_destroyer
    "tank_destroyer": {
        "aml90": 300,
        "amx-13-90": 340,
        "amx_15": 350,
        "brdm2_atgm": 250,
        "brdm2_atgm(ddr)": 250,
        "brdm2_atgm(nva)": 250,
        "brdm2_atgm(pol)": 250,
        "china63": 320,
        "elefant": 300,
        "fav": 250,
        "fox": 200,
        "fv101-90": 300,
        "fv107": 320,
        "hetzer": 100,
        "hummvee_tow": 200,
        "jagdpanther": 260,
        "jagdpanzer_iv": 240,
        "jagdtiger": 340,
        "kentavr": 350,
        "kentavr(eu)": 350,
        "m1128": 350,
        "m113a4": 200,
        "nashorn": 200,
        "pt76": 320,
        "pt76(nva)": 320,
        "pt76(pol)": 320,
        "sprut": 350,
        "stug3g": 120,
        "su-122-54(pol)": 350,
        "su100": 200,
        "tigr_ptur": 200,
        "toyota_hilux_spg9": 150,
        "type63_zdf-89": 270,
        "type63_zdf-89(nva)": 270,
        "uaz_spg9": 150,
        "uaz_spg9(pol)": 150,
        "vab-hot": 300,
        "vab-hot(eu)": 300,
        "zlf-92": 250
    },

    # aircraft
    "aircraft": {
        "apache": 650,
        "chinawz10": 700,
        "chinook": 400,
        "f4f": 800,
        "gazele": 650,
        "ka-50": 800,
        "mh-6_attack": 700,
        "mi-24v": 700,
        "mi-24v(ddr)": 700,
        "mi-24v(geo)": 400,
        "mi-24v(pol)": 800,
        "mi-24vm": 700,
        "mi17": 650,
        "mi17(ddr)": 600,
        "mi17(geo)": 500,
        "mi17(nva)": 750,
        "mi17(pol)": 600,
        "mi28": 750,
        "mi4": 650,
        "mq-9": 1200,
        "pumahel2": 600,
        "supercobra": 800,
        "tiger": 650,
        "tiger_b": 700,
        "uh-60": 700,
        "uh-60at": 650,
        "uh1": 600,
        "uh1_m60": 700,
        "uh1_mg3": 700,
        "uh1d": 750,
        "w-3": 700,
        "z-6": 600
    },

    # light_robot_mech
    "light_robot_mech": {
        "mvxx1": 300
    }
}
# ----------------------------------------------------------------

# Variables
fileToEditDirectory = r'.\FilesToEdit'


# Vehicle name pattern
vehicleNamePattern = r'{\"[a-zA-z0-9~@#$^*()_+=[\]|\\,.?:-]+\"'


# Helpers
# Formatting Helper: Gets filePath from file Name and Directory


def getFilePath(fileDirectory, fileName):
    return r'{filePath}\{fileName}'.format(filePath=fileDirectory, fileName=fileName)

# Vehicle Class Props/Property State Selection Helper: Gets appropriate replacement according to comment system


def classPropsSelection(line, vehiclePropsTable):
    # Loop through vehicleClass keys (first layer) in vehiclePropsTable
    for vehicleClass in vehiclePropsTable:
        # If vehicle Class is found in the current comment line
        # Vehicle Class Search Pattern must start and end with comment
        vehicleClassPattern = commentTrigger + vehicleClass + commentTrigger
        # return corresponding 2nd layer hash table of vehicle properties for that class
        if re.search(vehicleClassPattern, line):
            return vehiclePropsTable[vehicleClass]
    # If can't find a the class of vehicles, return DISABLING NONE default state
    return None

# search and Replace Helper: replaces patternToSearch with updateOptions


def searchAndReplace(patternToSearch, updateOptions):
    # Find vehicleName pattern block in line in the current line
    vehicleNameMatch = re.findall(vehicleNamePattern, line)
    # Extract out just the vehicle's name from the matched pattern
    if vehicleNameMatch:
        vehicleNameMatch = re.findall(
            r'[a-zA-z0-9~@#$^*()_+=[\]|\\,.?:-]+', vehicleNameMatch[0])
        # If vehicleName string found in current vehicle class updateOptions hash table
        if vehicleNameMatch[0] in updateOptions:
            # Get exact pattern to replace
            oldPropMatch = re.findall(replacementPattern, line)[0]
            # ----------------------------------------------------------------
            # Inputs (Edit new formatted replacement)
            # Create replacement
            newProp = 'cost {}'.format(
                str(updateOptions[vehicleNameMatch[0]]))
            # ----------------------------------------------------------------
            # Write line with replaced info
            print(line.replace(
                oldPropMatch, newProp), end='')
    else:
        # else (no match) rewrite unchanged line
        print(line, end='')


# Main Algorithm: Editting Logic

# Loop through files in Edit Folder
for fileName in os.listdir(fileToEditDirectory):
    # Open one of the files
    filePath = getFilePath(fileToEditDirectory, fileName)
    print('Editting: ', filePath)

    with fileinput.FileInput(filePath, inplace=True) as file:
        # For each line
        for line in file:
            # Trigger state change while searching through lines
            if line[0] == commentTrigger:
                classProps = classPropsSelection(line, vehiclePropsTable)

            # What to search for vs what to replace it with
            if classProps != None:
                searchAndReplace(replacementPattern, classProps)
            else:
                # else rewrite unchanged line
                print(line, end='')

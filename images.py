"""
Real vehicle photos for the app (hotlinked from Wikimedia Commons - stable, free URLs).

- VEHICLE_IMAGES  : image URL per vehicle name (exact match with vehicles.csv)
- CATEGORY_IMAGES : fallback image per category
- image_for()     : helper used by app.py and chatbot_widget.py

Note: URLs are used exactly as returned by the Wikimedia API (960px thumbnails or
unscaled originals for small files) - other hand-made sizes return HTTP 400.
"""
B = "https://upload.wikimedia.org/wikipedia/commons/thumb/"
U = "https://upload.wikimedia.org/wikipedia/commons/"

# ---- shared URLs ----
Mehr = U + "7/70/Mehran_Model_2001_Right_Side_View_At_Lowari_Pass%2CChitral%2CKPK.jpg"
CD70 = B + "4/4f/Honda_70_2025.jpg/960px-Honda_70_2025.jpg"
CG125 = B + "d/dc/%E3%83%9B%E3%83%B3%E3%83%80_CG125.jpg/960px-%E3%83%9B%E3%83%B3%E3%83%80_CG125.jpg"
YBR = B + "7/7f/Yamaha_YBR125_%28Fuel_Injection_-_EU_Spec%29.JPG/960px-Yamaha_YBR125_%28Fuel_Injection_-_EU_Spec%29.JPG"
Hiace = B + "8/80/2020_Toyota_HiAce_%28front%29.jpg/960px-2020_Toyota_HiAce_%28front%29.jpg"
Carry = B + "2/21/Suzuki_Carry_Truck_KC_4WD_DA16T.JPG/960px-Suzuki_Carry_Truck_KC_4WD_DA16T.JPG"
Civic22 = B + "b/b5/2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg/960px-2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg"
Civic17 = B + "6/6d/2017_Honda_Civic_SR_VTEC_1.0_Front.jpg/960px-2017_Honda_Civic_SR_VTEC_1.0_Front.jpg"
C172 = B + "a/ae/Cessna_172S_Skyhawk_SP%2C_Private_JP6817606.jpg/960px-Cessna_172S_Skyhawk_SP%2C_Private_JP6817606.jpg"
M2 = B + "0/0f/OO-FLN.JPG/960px-OO-FLN.JPG"
Rickshaw = U + "4/49/Bajaj_auto-rickshaw_in_Sri_Lanka.jpg"
Motorboat = B + "d/d9/Motorboat_at_Kankaria_lake.JPG/960px-Motorboat_at_Kankaria_lake.JPG"
HD883 = B + "4/4f/Flickr_-_ronsaunders47_-_HARLEY-DAVIDSON_XR1200_SPORTSTER._2010..jpg/960px-Flickr_-_ronsaunders47_-_HARLEY-DAVIDSON_XR1200_SPORTSTER._2010..jpg"
Orbea = B + "9/96/Orbea_Occam_2020.jpg/960px-Orbea_Occam_2020.jpg"
Chase = B + "5/58/Chase-ACT-Carbon-1.jpg/960px-Chase-ACT-Carbon-1.jpg"
Look795 = B + "6/66/Look_795_30th_Anniversary_Dura-Ace_9100-Mavic_Custom_Build_%2830636542393%29.jpg/960px-Look_795_30th_Anniversary_Dura-Ace_9100-Mavic_Custom_Build_%2830636542393%29.jpg"
Folding = B + "3/3d/1982_Hon_Convertible_folding_bicycle.JPG/960px-1982_Hon_Convertible_folding_bicycle.JPG"
Fatbike = B + "b/b9/Fat_bike.jpg/960px-Fat_bike.jpg"
Tandem = B + "9/90/Tandem_bike_with_double_electric_batteries.jpg/960px-Tandem_bike_with_double_electric_batteries.jpg"
Cyclocross = U + "2/20/Cyclocross_Fahrrad.jpg"
Ewheels = B + "b/b4/Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg/960px-Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg"
Aerox = B + "f/f3/Yamaha_Aerox_2011_.jpg/960px-Yamaha_Aerox_2011_.jpg"
Istock = U + "5/50/Istockphoto-114285168-612x612.jpg"
Corolla05 = B + "6/64/2005_Toyota_Corolla_%28ZZE122R_5Y%29_Ascent_sedan_01.jpg/960px-2005_Toyota_Corolla_%28ZZE122R_5Y%29_Ascent_sedan_01.jpg"
F250 = B + "8/83/2001_Ford_F-250_Super_Duty_XL_regular_cab_flatbed%2C_front_left%2C_05-17-2025.jpg/960px-2001_Ford_F-250_Super_Duty_XL_regular_cab_flatbed%2C_front_left%2C_05-17-2025.jpg"
Ford8N = B + "8/85/Ford_8N.jpg/960px-Ford_8N.jpg"
VHSUF = B + "7/70/VH-SUF_Taking_Off.jpg/960px-VH-SUF_Taking_Off.jpg"
YR1 = B + "1/1a/Yamaha_R1.jpg/960px-Yamaha_R1.jpg"
YR1b = B + "5/51/2015_Yamaha_YZF-R1_crop.JPG/960px-2015_Yamaha_YZF-R1_crop.JPG"
Transit = B + "1/1a/2018_Ford_Transit_Custom_300_Base_2.0_facelift.jpg/960px-2018_Ford_Transit_Custom_300_Base_2.0_facelift.jpg"
Minicab = B + "9/9e/Mitsubishi_Minicab_2000.jpg/960px-Mitsubishi_Minicab_2000.jpg"
Hilux = B + "1/1b/2016_Toyota_HiLux_Invincible_D-4D_4WD_2.4_Front.jpg/960px-2016_Toyota_HiLux_Invincible_D-4D_4WD_2.4_Front.jpg"
BusHino = B + "8/84/LTZ1328-19-20241030-160332.jpg/960px-LTZ1328-19-20241030-160332.jpg"
Elf = B + "6/6e/Nippon_Rent-A-Car_Isuzu_Elf_NJR85A.jpg/960px-Nippon_Rent-A-Car_Isuzu_Elf_NJR85A.jpg"
Jetski = B + "1/17/Couple_of_teenagers_riding_a_jetski_splashing_on_the_Mekong_in_Laos.jpg/960px-Couple_of_teenagers_riding_a_jetski_splashing_on_the_Mekong_in_Laos.jpg"
Yacht = B + "e/ef/White_Pearl_A_Seite.JPG/960px-White_Pearl_A_Seite.JPG"
R44 = B + "d/d5/Robinson_R44_II_%28cropped%29.jpg/960px-Robinson_R44_II_%28cropped%29.jpg"
R66 = B + "b/be/Robinson_R66_G-CIZG.jpg/960px-Robinson_R66_G-CIZG.jpg"
Bell407 = B + "4/4e/Nassau_County_Police_Bell_407.jpg/960px-Nassau_County_Police_Bell_407.jpg"

CATEGORY_IMAGES = {
    "Car": Corolla05,
    "Van": Transit,
    "Bus/Truck": F250,
    "Tractor": Ford8N,
    "Rickshaw": Rickshaw,
    "Petrol Bike": Istock,
    "Heavy Bike": YR1,
    "Scooter": Aerox,
    "Electric Bike": Ewheels,
    "Cycle": Orbea,
    "Boat": Motorboat,
    "Helicopter": VHSUF,
    "Aircraft": C172,
    "Jet": M2,
}

VEHICLE_IMAGES = {
    # ================= CARS =================
    "Suzuki Alto VXR": B + "5/55/1994-1997_Suzuki_Alto.jpg/960px-1994-1997_Suzuki_Alto.jpg",
    "Suzuki Alto VXL AGS": B + "5/55/1994-1997_Suzuki_Alto.jpg/960px-1994-1997_Suzuki_Alto.jpg",
    "Suzuki Cultus VXL": B + "f/f8/2nd_generation_Suzuki_Cultus.jpg/960px-2nd_generation_Suzuki_Cultus.jpg",
    "Suzuki Wagon R VXL AGS": B + "3/35/1996_Suzuki_Wagon_R_RX_in_Radiant_Red_Mica%2C_front_left.jpg/960px-1996_Suzuki_Wagon_R_RX_in_Radiant_Red_Mica%2C_front_left.jpg",
    "Suzuki Swift GLX CVT": B + "3/3d/Suzuki_Swift_%282024%29_hybrid_DSC_6076.jpg/960px-Suzuki_Swift_%282024%29_hybrid_DSC_6076.jpg",
    "Toyota Yaris GLI CVT": B + "f/f5/2015_Toyota_Yaris_1.5_G_hatchback_%28NCP150R%3B_12-22-2018%29%2C_South_Tangerang.jpg/960px-2015_Toyota_Yaris_1.5_G_hatchback_%28NCP150R%3B_12-22-2018%29%2C_South_Tangerang.jpg",
    "Toyota Corolla Altis Grande": B + "a/a4/2016_Toyota_Corolla_%28ZRE172R%29_Ascent_sedan_%282017-01-15%29_01.jpg/960px-2016_Toyota_Corolla_%28ZRE172R%29_Ascent_sedan_%282017-01-15%29_01.jpg",
    "Toyota Corolla Cross HEV": B + "4/43/2023_Toyota_Corolla_Cross_XLE_4WD_in_Wind_Chill_Pearl%2C_front_left.jpg/960px-2023_Toyota_Corolla_Cross_XLE_4WD_in_Wind_Chill_Pearl%2C_front_left.jpg",
    "Toyota Fortuner Sigma 4": B + "6/66/2015_Toyota_Fortuner_%28New_Zealand%29.jpg/960px-2015_Toyota_Fortuner_%28New_Zealand%29.jpg",
    "Toyota Land Cruiser ZX": B + "6/6d/2021_Toyota_Land_Cruiser_300_3.4_ZX_%28Colombia%29_front_view_04.png/960px-2021_Toyota_Land_Cruiser_300_3.4_ZX_%28Colombia%29_front_view_04.png",
    "Toyota Hilux Revo 2.8": Hilux,
    "Toyota Rush": B + "9/97/2018_Daihatsu_Terios_1.5_R_Deluxe_wagon_%28F800RG%3B_01-12-2019%29%2C_South_Tangerang.jpg/960px-2018_Daihatsu_Terios_1.5_R_Deluxe_wagon_%28F800RG%3B_01-12-2019%29%2C_South_Tangerang.jpg",
    "Toyota Yaris Cross": B + "8/85/2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg/960px-2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg",
    "Honda City 1.2 M/T": B + "e/e7/Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg/960px-Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg",
    "Honda City RS 1.5 CVT": B + "e/e7/Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg/960px-Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg",
    "Honda Civic Oriel Turbo": Civic17,
    "Honda Civic RS e:HEV": Civic22,
    "Honda HR-V VTI": B + "7/71/2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg/960px-2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg",
    "Honda Vezel Hybrid (used import)": B + "7/71/2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg/960px-2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg",
    "Honda N Wgn (used import)": B + "0/03/Honda_N-WGN_G_%28JH1%29_front.JPG/960px-Honda_N-WGN_G_%28JH1%29_front.JPG",
    "Honda Fit Hybrid (used import)": B + "8/85/Honda_Jazz_Hybrid_Executive_%28IV%29_%E2%80%93_f_18102020.jpg/960px-Honda_Jazz_Hybrid_Executive_%28IV%29_%E2%80%93_f_18102020.jpg",
    "Toyota Vitz (used import)": B + "8/85/2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg/960px-2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg",
    "Toyota Aqua (used import)": B + "d/d8/2017-2021_Toyota_Aqua.jpg/960px-2017-2021_Toyota_Aqua.jpg",
    "Toyota Prius S (used import)": B + "7/71/2018_Toyota_Prius_Excel_VVT-i_CVT_1.8.jpg/960px-2018_Toyota_Prius_Excel_VVT-i_CVT_1.8.jpg",
    "Suzuki Mehran (used)": Mehr,
    "Daihatsu Mira (used import)": B + "d/dd/7th_generation_Daihatsu_Mira_01.jpg/960px-7th_generation_Daihatsu_Mira_01.jpg",
    "Mitsubishi Ek Wagon (used import)": B + "8/8c/Mitsubishi_eK_wagon_G_%285BA-B33W-LTCE%29_front.jpg/960px-Mitsubishi_eK_wagon_G_%285BA-B33W-LTCE%29_front.jpg",
    "Suzuki Spacia (used import)": B + "c/c3/Spacia-mk42s-4WD-with-foglamps.jpg/960px-Spacia-mk42s-4WD-with-foglamps.jpg",
    "KIA Picanto 1.0 MT": B + "8/8d/2018_Kia_Picanto_3_Automatic_1.2_Front.jpg/960px-2018_Kia_Picanto_3_Automatic_1.2_Front.jpg",
    "KIA Sportage Alpha": B + "5/5d/2025_Kia_Sportage_S_front_only.jpg/960px-2025_Kia_Sportage_S_front_only.jpg",
    "KIA Sorento FWD": B + "8/84/2024_Kia_Sorento_X-Line_SX_Prestige_%28facelift%29%2C_front_12.20.24.jpg/960px-2024_Kia_Sorento_X-Line_SX_Prestige_%28facelift%29%2C_front_12.20.24.jpg",
    "KIA Stonic EX": B + "7/74/2017_Kia_Stonic_First_Edition_1.0.jpg/960px-2017_Kia_Stonic_First_Edition_1.0.jpg",
    "KIA K5 GT Line": Corolla05,
    "Hyundai Tucson FWD": B + "6/61/Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_%28IV%29_%E2%80%93_f_05072025.jpg/960px-Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_%28IV%29_%E2%80%93_f_05072025.jpg",
    "Hyundai Santa Fe FWD": B + "e/e6/2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey%2C_front_left%2C_2024-06-30.jpg/960px-2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey%2C_front_left%2C_2024-06-30.jpg",
    "Hyundai Elantra GLS": B + "a/a4/2023_Hyundai_Elantra_Limited_in_Silver%2C_front_left%2C_04-04-2026.jpg/960px-2023_Hyundai_Elantra_Limited_in_Silver%2C_front_left%2C_04-04-2026.jpg",
    "MG ZS EV": B + "c/cf/MG_ZS_%28crossover%2C_second_generation%29_DSC_8542.jpg/960px-MG_ZS_%28crossover%2C_second_generation%29_DSC_8542.jpg",
    "MG HS": B + "3/38/MG_HS_Hybrid%2B_Luxury_%28II%29_%E2%80%93_f_12032026.jpg/960px-MG_HS_Hybrid%2B_Luxury_%28II%29_%E2%80%93_f_12032026.jpg",
    "MG 5 (used import)": B + "e/ef/2020_SAIC_MG_5_%28front%29.jpg/960px-2020_SAIC_MG_5_%28front%29.jpg",
    "Changan Alsvin 1.5": B + "6/61/2018_Chang%27an_Alsvin_%28front%29.jpg/960px-2018_Chang%27an_Alsvin_%28front%29.jpg",
    "Changan Oshan X7": Transit,
    "Haval H6 HEV": B + "4/4e/Haval_H6_III_IMG001_%28cropped%29.jpg/960px-Haval_H6_III_IMG001_%28cropped%29.jpg",
    "Haval Jolion HEV": B + "a/ac/2020_Great_Wall_Haval_Jolion_%28front%29.jpg/960px-2020_Great_Wall_Haval_Jolion_%28front%29.jpg",
    "BYD Atto 3 EV": B + "3/3e/BYD_Atto_3_1X7A6491.jpg/960px-BYD_Atto_3_1X7A6491.jpg",
    "BYD Seal EV": B + "3/3e/BYD_Atto_3_1X7A6491.jpg/960px-BYD_Atto_3_1X7A6491.jpg",
    "Chery Tiggo 4 Pro": B + "7/76/Chery_Tiggo_7_II_014_%28cropped%29.jpg/960px-Chery_Tiggo_7_II_014_%28cropped%29.jpg",
    "Chery Tiggo 8 Pro": B + "7/76/Chery_Tiggo_7_II_014_%28cropped%29.jpg/960px-Chery_Tiggo_7_II_014_%28cropped%29.jpg",
    "Omoda C5": B + "7/76/Chery_Tiggo_7_II_014_%28cropped%29.jpg/960px-Chery_Tiggo_7_II_014_%28cropped%29.jpg",
    "Ora 03 EV": B + "1/1c/GWM_Ora_03_%E2%80%93_f_12102025.jpg/960px-GWM_Ora_03_%E2%80%93_f_12102025.jpg",
    "Jaecoo J7 PHEV": B + "6/63/Jaecoo_J7_1.6T_4WD_%E2%80%93_f_21032025.jpg/960px-Jaecoo_J7_1.6T_4WD_%E2%80%93_f_21032025.jpg",
    "Jetour Dashing 1.5T": B + "1/17/Jetour_Dashing_006.jpg/960px-Jetour_Dashing_006.jpg",
    "Jetour X70 Plus": B + "5/54/Jetour_X70_Plus_facelift_001_%28cropped%29.jpg/960px-Jetour_X70_Plus_facelift_001_%28cropped%29.jpg",
    "Deepal S07 EV": B + "5/59/2023_Chang%27an_Shenlan_S7.jpg/960px-2023_Chang%27an_Shenlan_S7.jpg",
    "Zeekr 001 (imported)": B + "0/0a/2022_Zeekr_001_%28front%29.jpg/960px-2022_Zeekr_001_%28front%29.jpg",
    "Audi A6 45 TFSI (imported)": B + "e/eb/Audi_A6_C9_IAA_2025_DSC_1920.jpg/960px-Audi_A6_C9_IAA_2025_DSC_1920.jpg",
    "Audi e-tron 50 (used import)": B + "d/d5/2020_Audi_e-Tron_Sport_50_Quattro.jpg/960px-2020_Audi_e-Tron_Sport_50_Quattro.jpg",
    "BMW 520i (imported)": B + "8/86/BMW_G60_520i_1X7A2443.jpg/960px-BMW_G60_520i_1X7A2443.jpg",
    "BMW 330i M Sport (imported)": B + "8/86/BMW_G60_520i_1X7A2443.jpg/960px-BMW_G60_520i_1X7A2443.jpg",
    "Mercedes-Benz E200 (imported)": B + "f/fd/Mercedes-Benz_W214_1X7A1841.jpg/960px-Mercedes-Benz_W214_1X7A1841.jpg",
    "Mercedes-Benz S500 (imported)": B + "0/09/2026_Mercedes-Benz_V223_IMG_7632.jpg/960px-2026_Mercedes-Benz_V223_IMG_7632.jpg",
    "Tesla Model 3 (used import)": B + "a/ab/Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg/960px-Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg",
    "Range Rover Sport (used import)": B + "a/aa/2015_Land_Rover_Range_Rover_Sport_HSE_3.0_Front.jpg/960px-2015_Land_Rover_Range_Rover_Sport_HSE_3.0_Front.jpg",
    "Lexus LX 570 (used import)": B + "3/34/2018_Lexus_LX_570_%28facelift%29%2C_front_3.24.23.jpg/960px-2018_Lexus_LX_570_%28facelift%29%2C_front_3.24.23.jpg",
    "Rolls-Royce Cullinan (imported)": B + "0/0d/2019_Rolls-Royce_Cullinan_V12_Automatic_6.75_Front.jpg/960px-2019_Rolls-Royce_Cullinan_V12_Automatic_6.75_Front.jpg",
    # ================= VANS =================
    "Suzuki Bolan VX": Carry,
    "Toyota Hiace Grand Cabin": Hiace,
    "Changan Karvaan Plus": Minicab,
    "Nissan Clipper (used import)": Carry,
    "Suzuki Every (used import)": B + "7/76/Suzuki_Every_DA17V_PA_Limited.jpg/960px-Suzuki_Every_DA17V_PA_Limited.jpg",
    "Mitsubishi Minicab (used import)": Minicab,
    # ================= BUS / TRUCK =================
    "Passenger Bus (Hino class)": BusHino,
    "Isuzu NPR Truck": Elf,
    # ================= TRACTORS =================
    "New Holland Fiat 480": Ford8N,
    "Massey Ferguson MF-385": Ford8N,
    "Millat MF-240": Ford8N,
    # ================= RICKSHAWS =================
    "Sazgar Auto Rickshaw CNG": Rickshaw,
    "Bajaj Auto Rickshaw CNG": Rickshaw,
    "Electric Passenger Rickshaw": Rickshaw,
    "Qingqi Loader Rickshaw": Rickshaw,
    # ================= PETROL BIKES =================
    "Honda CD 70": CD70,
    "Honda CD 70 Dream": CD70,
    "Honda CG 125": CG125,
    "Honda CG 125 Self Start": CG125,
    "Honda Pridor 100": Istock,
    "Honda CB 125F": B + "6/6d/Honda_CBF125_2009.jpg/960px-Honda_CBF125_2009.jpg",
    "Honda CB 150F": Istock,
    "Yamaha YBR 125": YBR,
    "Yamaha YBR 125G": YBR,
    "Yamaha YB 125Z": Istock,
    "Suzuki GD 110S": Istock,
    "Suzuki GS 150": Istock,
    "Suzuki GSX 125": B + "5/5a/Suzuki_EN125_Thunder.jpg/960px-Suzuki_EN125_Thunder.jpg",
    "Road Prince RP 110": Istock,
    "United US 125": Istock,
    # ================= SCOOTERS =================
    "Honda Activa 6G (imported)": B + "e/ec/Gold_Metallic_Honda_Activa.jpg/960px-Gold_Metallic_Honda_Activa.jpg",
    "Suzuki Access 125 (imported)": B + "4/4d/BURGMAN650_K6.JPG/960px-BURGMAN650_K6.JPG",
    "Vespa 150 (imported)": B + "b/b8/PerthVespa.jpg/960px-PerthVespa.jpg",
    "Yamaha Zuma 125 (imported)": B + "0/0c/MBK_Booster%2C_yellow.jpg/960px-MBK_Booster%2C_yellow.jpg",
    # ================= ELECTRIC BIKES =================
    "Electric Cycle (pedal assist)": Ewheels,
    "Vlektra Bolt 180": Ewheels,
    "Jolta JE-70L": Ewheels,
    # ================= HEAVY BIKES =================
    "Honda CB 350 (imported)": B + "e/ec/Honda_350.jpg/960px-Honda_350.jpg",
    "KTM Duke 200 (imported)": B + "1/14/2020_Duke_200.jpg/960px-2020_Duke_200.jpg",
    "KTM Duke 390 (imported)": B + "8/8d/Ktm_duke_390.jpg/960px-Ktm_duke_390.jpg",
    "Kawasaki Ninja 400 (imported)": B + "8/8b/2026-06-27_Moscow_electric_vehicle_parade%2C_display_20_Kawasaki_Ninja.jpg/960px-2026-06-27_Moscow_electric_vehicle_parade%2C_display_20_Kawasaki_Ninja.jpg",
    "Kawasaki Z900 (imported)": B + "b/bc/Kawasaki_Z900%2C_green.jpg/960px-Kawasaki_Z900%2C_green.jpg",
    "Honda CBR 650R (imported)": B + "f/ff/2023_Honda_CBR650R_E-Clutch.jpg/960px-2023_Honda_CBR650R_E-Clutch.jpg",
    "Honda CB 500F (imported)": B + "7/77/2023_Honda_CB500_Hornet.jpg/960px-2023_Honda_CB500_Hornet.jpg",
    "Yamaha YZF R1 (used import)": YR1b,
    "Suzuki Hayabusa (imported)": B + "d/de/SUZUKI_Hayabusa_2007TMS.jpg/960px-SUZUKI_Hayabusa_2007TMS.jpg",
    "BMW S 1000 RR (used import)": B + "d/d5/BMW_S_1000_RR_-_BMW_M_1000_RR_50_Years_M_%2822121615413%29.jpg/960px-BMW_S_1000_RR_-_BMW_M_1000_RR_50_Years_M_%2822121615413%29.jpg",
    "Harley-Davidson Iron 883 (used import)": HD883,
    # ================= CYCLES (har cycle ki alag photo) =================
    "Road Racing Bicycle": Look795,
    "Orbea Mountain Bike": Orbea,
    "BMX Stunt Bike": Chase,
    "Fat Bike 26 inch": Fatbike,
    "Folding Bicycle": Folding,
    "Tandem Bicycle": Tandem,
    "Cyclo-cross Bicycle": Cyclocross,
    # ================= BOATS =================
    "Motor Boat (small)": Motorboat,
    "Speed Boat 200HP": Motorboat,
    "Jet Ski": Jetski,
    "Luxury Yacht (small)": Yacht,
    # ================= HELICOPTERS =================
    "Robinson R22 Helicopter": VHSUF,
    "Robinson R44 Helicopter": R44,
    "Robinson R66 Turbine Helicopter": R66,
    "Bell 407 Helicopter": Bell407,
    # ================= AIRCRAFT =================
    "Cessna 172 Skyhawk": C172,
    "Piper PA-28 Cherokee (used)": B + "1/17/G-AVRZ_Piper_PA-28-180_Cherokee_C_at_Northrepps.jpg/960px-G-AVRZ_Piper_PA-28-180_Cherokee_C_at_Northrepps.jpg",
    "Diamond DA40 (used)": B + "c/c1/Diamond_DA40_%288736184864%29.jpg/960px-Diamond_DA40_%288736184864%29.jpg",
    # ================= JETS =================
    "Cessna Citation M2 Light Jet": M2,
    "Embraer Phenom 300E": B + "8/8f/Embraer_505_Phenom_300%2C_Aerojet_JP7625910.jpg/960px-Embraer_505_Phenom_300%2C_Aerojet_JP7625910.jpg",
    "Gulfstream G650 Private Jet": B + "d/d6/G-ULFS_Gulfstream_G650_CVT_05-05-16_%2827046023031%29_%28cropped%29.jpg/960px-G-ULFS_Gulfstream_G650_CVT_05-05-16_%2827046023031%29_%28cropped%29.jpg",
}


def image_for(name, category):
    """Photo URL for a vehicle; falls back to its category photo, then ''."""
    return VEHICLE_IMAGES.get(name) or CATEGORY_IMAGES.get(category, "")


def small_url(url):
    """Fast-loading small (480px) version of a Wikimedia URL.

    Works for both /thumb/.../960px-FILE urls and unscaled commons urls.
    NOTE: the 480px url is only an ATTEMPT - some networks/proxies block
    hand-made thumb sizes (HTTP 400). The app therefore always pairs it
    with the verified original via the <img onerror> fallback, so a
    blocked small url can never leave a broken image on screen.
    """
    if not url:
        return ""
    if "/thumb/" in url:
        for size in ("960px-", "800px-", "640px-", "500px-"):
            if size in url:
                return url.replace(size, "480px-", 1)
        return url
    # unscaled original like .../commons/7/70/File.jpg -> build a thumb url
    try:
        rest = url.split("/commons/", 1)[1]           # 7/70/File.jpg
        fname = rest.rsplit("/", 1)[1]
        return B + rest + "/480px-" + fname
    except IndexError:
        return url


def pair_for_url(url):
    """(small_fast_attempt, verified_original) for an <img onerror> pattern."""
    return small_url(url), (url or "")

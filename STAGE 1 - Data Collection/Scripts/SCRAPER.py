# IMPORT LIBRARIES
import pandas as pd
from time import sleep
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# FUNCTION TO OPEN WEB DRIVER
def open_browser(start_date, end_date, bedroom):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)

    # URL WITH ADJUSTABLE PARAMETERS (CHANGEABLE)
    url = f'https://ar.airbnb.com/s/Riyadh--Saudi-Arabia/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJmZNIDYkDLz4R1Z_nmBxNl7o&checkin={start_date}&checkout={end_date}&adults=1&tab_id=home_tab&query=Riyadh%2C%20Saudi%20Arabia&flexible_trip_lengths%5B%5D=one_week&monthly_start_date={start_date}&monthly_length=3&monthly_end_date={end_date}&search_mode=regular_search&disable_auto_translation=true&price_filter_input_type=1&price_filter_num_nights=30&channel=EXPLORE&min_bedrooms={bedroom}&search_type=filter_change&_set_bev_on_new_domain=1719411835_EANDIzMGUxZGQ2ZT&enable_auto_translate=true'
    browser.get(url)
    return browser

# FUNCTION TO NAVIGATE TO NEXT PAGE
def navigate_to_next_page(browser):

    # NEXT PAGE BUTTON (CHANGEABLE)
    next_button_xpath = '//div[@class="p1j2gy66 atm_9s_1txwivl dir dir-rtl"]/a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 c1ytbx3a atm_mk_h2mmj6 atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_26_1j28jx2 atm_3f_glywfm atm_7l_hkljqm atm_gi_idpfg4 atm_l8_idpfg4 atm_uc_10d7vwn atm_kd_glywfm atm_gz_8tjzot atm_uc_glywfm__1rrf6b5 atm_26_zbnr2t_1rqz0hn_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_zbnr2t_1ul2smo atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_70_glywfm_1w3cfyq atm_uc_aaiy6o_9xuho3 atm_70_18bflhl_9xuho3 atm_26_zbnr2t_9xuho3 atm_uc_glywfm_9xuho3_1rrf6b5 atm_70_glywfm_pfnrn2_1oszvuo atm_uc_aaiy6o_1buez3b_1oszvuo atm_70_18bflhl_1buez3b_1oszvuo atm_26_zbnr2t_1buez3b_1oszvuo atm_uc_glywfm_1buez3b_1o31aam atm_7l_1wxwdr3_1o5j5ji atm_9j_13gfvf7_1o5j5ji atm_26_1j28jx2_154oz7f atm_92_1yyfdc7_vmtskl atm_9s_1ulexfb_vmtskl atm_mk_stnw88_vmtskl atm_tk_1ssbidh_vmtskl atm_fq_1ssbidh_vmtskl atm_tr_pryxvc_vmtskl atm_vy_1vi7ecw_vmtskl atm_e2_1vi7ecw_vmtskl atm_5j_1ssbidh_vmtskl atm_mk_h2mmj6_1ko0jae dir dir-rtl"]'

    try:
        # WAIT FOR NEXT BUTTON TO BE CLICKABLE
        sleep(5)
        next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
        next_button.click()
    except TimeoutException:
        pass

# FUNCTION TO SCRAPE SITE TO GET SPECIFIC DATA (NAME, DISTRICT, PRICE, LINK)
def scrape_data(browser):

    # LISTS TO STORE DATA
    name_list = []
    district_list = []
    price_list = []
    url_list = []

    try:
        # GET NAME OF PROPERTIES BY XPATH (CHANGEABLE)
        try:
            name_elements = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//span[@data-testid="listing-card-name"]')))
            for name_element in name_elements:
                name = name_element.text
                name_list.append(name)
        except TimeoutException:
            pass

        # GET DISTRICT OF PROPERTIES BY XPATH (CHANGEABLE)
        try:
            district_elements = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="listing-card-title"]')))
            for district_element in district_elements:
                district = district_element.text
                district_list.append(district)
        except TimeoutException:
            pass

        # GET PRICE OF PROPERTIES BY XPATH (CHANGEABLE)
        try:
            price_elements = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//span[contains(@class,"_11jcbg2")]')))
            for price_element in price_elements:
                price = price_element.text
                price_list.append(price)
        except TimeoutException:
            pass

        # GET URL OF PROPERTIES BY XPATH (CHANGEABLE)
        try:
            properties = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]/a')))
            url_list = [prop.get_attribute("href") for prop in properties]
        except TimeoutException:
            pass

            # ENSURE ALL DATA IS THE SAME LENGTH TO HANDLE MISMATCHES
            if len(name_list) == len(district_list) == len(price_list) == len(url_list):
                return district_list, price_list, name_list, url_list
            else:
                return [], [], [], []
    except TimeoutException:
        return [], [], [], []

    return district_list, price_list, name_list, url_list

# FUNCTION TO MAKE DATAFRAME FROM SCRAPED DATA
def extract_dataframe(district_list, price_list, name_list, url_list, start_dates, end_dates, bedroom):

    # ENSURE ALL DATA IS THE SAME LENGTH TO HANDLE MISMATCHES
    min_length = min(len(district_list), len(price_list), len(name_list), len(url_list), len(start_dates),len(end_dates), len(bedroom))

    df = pd.DataFrame({
        "Name": name_list[:min_length],
        "District": district_list[:min_length],
        "Price": price_list[:min_length],
        "Bedroom": bedroom[:min_length],
        "Start_Date": start_dates[:min_length],
        "End_Date": end_dates[:min_length],
        "URL": url_list[:min_length]
    })

    return df


# FUNCTION TO TRANSFER DATAFRAME TO EXCEL FORMAT
def save_to_excel(df, file):
    df.to_excel(file, index=False)
    print(f"DATA SAVED TO {file}")

# EXECUTION CODE TO INTEGRATE ALL THE FUNCTIONS
def execute_code(start_date_str, end_date_str, bedroom):

    # CONVERT START DATE, END DATE FROM STRING TO DATETIME
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # LISTS TO STORE DATA
    all_names = []
    all_districts = []
    all_prices = []
    all_urls = []
    all_bedrooms = []
    all_start_dates = []
    all_end_dates = []

    # LOOP THROUGH DATES AND STOP IN SPECIFIC DATE (CHANGEABLE)
    while end_date <= datetime.strptime('2024-12-31', '%Y-%m-%d'):

        # COVERT TO DATE BACK TO STRING FORMAT
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # OPEN BROWSER
        browser = open_browser(start_date_str, end_date_str, bedroom)

        # SCRAPE THROUGH RANGE OF PAGES (CHANGEABLE)
        for page in range(15):
            districts, prices, names, urls = scrape_data(browser)
            all_districts.extend(districts)
            all_prices.extend(prices)
            all_names.extend(names)
            all_urls.extend(urls)
            all_start_dates.extend([start_date_str] * len(names))
            all_end_dates.extend([end_date_str] * len(names))
            all_bedrooms.extend([bedroom] * len(names))

            # NAVIGATE TO NEXT PAGE
            navigate_to_next_page(browser)

        # CLOSE BROWSER
        browser.quit()

        # INCREMENT START_DATE AND END_DATE BY ONE TO BE DAY BY DAY
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)

    # EXTRACT FINAL DATAFRAME
    df = extract_dataframe(all_districts, all_prices, all_names, all_urls, all_start_dates, all_end_dates, all_bedrooms)
    file = '../Datasets/(12) December/AirBnB_Riyadh_(12)December_Bedroom(3).xlsx'
    save_to_excel(df, file)

if __name__ == "__main__":
    start_date = '2024-12-01'
    end_date = '2024-12-02'
    bedroom = 3
    execute_code(start_date, end_date, bedroom)
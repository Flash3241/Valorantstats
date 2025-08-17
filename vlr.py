from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

player_name = input("Enter player name: ").strip()
kill_line = float(input("Enter kill line to evaluate: ").strip())
PATH = r"C:\Program Files (x86)\chromedriver.exe"  # raw string to handle backslashes

service = Service(PATH)
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")  # additional option to prevent popups

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://www.vlr.gg/')
    
    # Wait for and click the search bar
    search = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ui-autocomplete-input"))
    )
    search.send_keys("Sentinels")
    search.send_keys(Keys.RETURN)
    
    # Click first result
    first_result = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.wf-module-item.search-item.mod-first"))
    )
    first_result.click()
    
    # Click matches tab
    matches_tab = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.wf-nav-item.mod-matches"))
    )
    matches_tab.click()
    
    # Get match cards
    match_cards = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.wf-card.fc-flex.m-item"))
    )
    total_kills = []
    # Get last 5 games
    last_5 = match_cards[-5:] if len(match_cards) >= 5 else match_cards
    
    for i, card in enumerate(last_5, 1):
        try:
            url = card.get_attribute("href")
            print(f"\nChecking Game {i}: {url}")
            
            # Open in new tab to avoid back navigation issues
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            
            # Wait for match page
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".match-header-vs"))
            )
            
            # Find all player rows
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
            )
            
            found = False
            for row in rows:
                try:
                    name_cell = row.find_element(By.CSS_SELECTOR, "td.mod-player")
                    name_text = name_cell.text.strip().split("\n")[0]
                    
                    if player_name.lower() in name_text.lower():
                        kills = row.find_element(
                            By.CSS_SELECTOR,
                            "td.mod-stat.mod-kills span, td.mod-stat.mod-vlr-kills span"
                        ).text.strip()
                        print(f"{name_text} had {kills} kills in this game.")
                        total_kills.append(int(kills))
                        found = True
                        break
                except Exception as e:
                    continue

            if not found:
                print(f"Could not find kill data for {player_name} in this match.")
            
            # Close current tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)  # brief pause
            
            print("\nKill Summary:")
            print(f"Total kills collected: {total_kills}")
            print(f"Average kills: {sum(total_kills)/len(total_kills):.1f}" if total_kills else "No kills data")
                # ---- Hit rate calculation ----
            if total_kills:
                hits = sum(1 for k in total_kills if k >= kill_line)
                hit_rate = hits / len(total_kills)

                print("\nHit Rate (based on last 5 games):")
                print(f"Line: {kill_line:g} kills")
                print(f"Games ≥ line: {hits}/{len(total_kills)}")
                print(f"Estimated probability of clearing line next game: {hit_rate*100:.1f}%")

                # Optional: 95% confidence interval
                n = len(total_kills)
                z = 1.96
                phat = hit_rate
                denom = 1 + z**2/n
                center = (phat + z**2/(2*n)) / denom
                margin = z * math.sqrt((phat*(1-phat)/n) + (z**2/(4*n**2))) / denom
                lo, hi = max(0.0, center - margin), min(1.0, center + margin)
                print(f"95% CI: [{lo*100:.1f}%, {hi*100:.1f}%]")
            else:
                print("\nNo kills data to compute a hit rate.")

        except Exception as e:
            print(f"Error processing game {i}: {str(e)}")
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
    
except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()
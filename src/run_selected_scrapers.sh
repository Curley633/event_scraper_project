#!/bin/bash

check_scraper_source() {
    if [ "${scraper_source}" == "DME" ]; then
        echo "SCRAPER SOURCE = ${scraper_source} SCRAPER"
        python3 "src/DME_Scraper.py"
    elif [[ ${scraper_source} == "BLABBERMOUTH" ]]; then
        echo "SCRAPER SOURCE = ${scraper_source} SCRAPER"
        python3 "src/Blabbermouth_Scraper.py"
    elif [[ ${scraper_source} == "TICKETMASTER" ]]; then
        echo "SCRAPER SOURCE = ${scraper_source} SCRAPER"
        python3 "src/Ticketmaster_Scraper.py"
    elif [[ ${scraper_source} == "METALCELL" ]]; then
        echo "SCRAPER SOURCE = ${scraper_source} SCRAPER"
        python3 "src/Metal_Cell_Scraper.py"
    elif [[ ${scraper_source} == "MONROES" ]]; then
        echo "SCRAPER SOURCE = ${scraper_source} SCRAPER"
        python3 "src/Monroes_Scraper.py"
    else
        echo "RUNNING ALL SCRAPERS"
        python3 "src/DME_Scraper.py"
        python3 "src/Monroes_Scraper.py"
        python3 "src/Ticketmaster_Scraper.py"
        python3 "src/Blabbermouth_Scraper.py"
        python3 "scc/Metal_Cell_Scraper.py"
    fi
}

scraper_source="${1}"
echo "${scraper_source}"
check_scraper_source
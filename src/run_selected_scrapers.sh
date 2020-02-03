#!/bin/bash

#inject_properties() {
#     Check if File exists and is greater than size zero
#    properties_file=$1
#    if [[ -f "${properties_file}" ]] && [[ -s "${properties_file}" ]]; then
#        echo "Sourcing the following variables from ${properties_file}:"
#        cat "${properties_file}"
#        source "${properties_file}"
#    else
#        echo "ERROR : Issue finding the file or file size is zero (${properties_file})."
#        echo "Please pass in a valid properties file"
#        exit 1
#    fi
#    echo -e "\n"
#}

check_scraper_source() {
    if [[ ${scraper_source} == "DME" ]]; then
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
#        python3 "scr/Metal_Cell_Scraper.py"
    fi
}

scraper_source="${1}"
echo "${scraper_source}"
#inject_properties "${build_parameters_file}"
check_scraper_source
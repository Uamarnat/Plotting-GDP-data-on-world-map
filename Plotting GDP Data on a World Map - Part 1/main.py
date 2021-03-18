import csv
import math
import pygal

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    reconcile_dict = {}
    reconcile_set = set()
    for key, value in plot_countries.items():
        for name in gdp_countries:

            if value == name:
                reconcile_dict[key] = name

        if value not in gdp_countries:
            reconcile_set.add(key)
    reconcile_tup = (reconcile_dict, reconcile_set)
    return reconcile_tup

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    nested_dict={}
    with open(gdpinfo["gdpfile"]) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=gdpinfo["separator"], quotechar=gdpinfo["quote"])
        for row in reader:
            nested_dict[row[gdpinfo["country_name"]]] = row
    log_dict = {}
    set1 = set()
    set2 = set()
    for code, country in plot_countries.items():
        if country in nested_dict.keys():
            if nested_dict[country][year] == "":
                set2.add(code)
            else:
                log_dict[code] = math.log10(float(nested_dict[country][year]))
        else:
            set1.add(code)

    return (log_dict, set1, set2)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    mapdata = build_map_dict_by_name(gdpinfo, plot_countries, year)
    gdpdict = mapdata[0]  # the GDP dictionary
    notinfile = mapdata[1]  # set of country codes not present in file
    nogdp = mapdata[2]  # set of country's with no gdp value

    worldmap = pygal.maps.world.World()
    worldmap.title = "GDP by country for " + year + " (log scale), " + "unified by common country NAME"
    # shades of counties are different between all three adds or datasets
    worldmap.add("GDP for " + year, gdpdict)
    worldmap.add("Missing from World Bank Data", notinfile)
    worldmap.add("No GDP data", nogdp)
    worldmap.render_to_file(map_file)
    return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")

test_render_world_map()
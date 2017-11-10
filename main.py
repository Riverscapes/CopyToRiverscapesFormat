import os
import re
from os.path import dirname, isfile
import shutil
from flow_row_object import FlowRowObject


fis_model_path = "C:\Users\A02150284\Downloads\FuzzyHSI\FuzzyHSI"
analyses_from_path = "C:\Users\A02150284\Downloads\Habitat"


def search_and_copy(from_root, to_root, from_regex, new_name="None"):
    """
    Copies every file in the from_root that matches the regex into the to_root. Renames the file if new_name != "None"
    :param from_root:
    :param to_root:
    :param from_regex:
    :param new_name:
    :return: None
    """
    if not os.path.exists(from_root):
        print from_root
        return
    elif not os.path.exists(to_root):
        print to_root
        return

    for file in os.listdir(from_root):
        match = re.match(from_regex, file)
        if match:
            data = match.groups()
            if new_name == "None":
                shutil.copy2(from_root + '\\' + file, to_root)
            else:
                shutil.copy2(from_root + '\\' + file, to_root + "\\" + new_name + "." + data[1])


def set_up_inputs(visit_to_path, visit_from_path):
    """
    Sets up the input folder
    :param visit_to_path: The folder that we want to copy our data to
    :param visit_from_path: The folder that we want to copy our data from
    :return:
    """
    input_to_path = visit_to_path + "\\Inputs"
    if not os.path.exists(input_to_path):
        os.makedirs(input_to_path)

    FIS_from_path = visit_from_path + "\\Sims\\FIS"

    input_from_path = "None"
    # checks if there are any directories that have "input" in their name (not case sensitive), and sets them as the
    # from directory
    for root, dirs, files in os.walk(FIS_from_path):
        input_regex = r'(?i)input'
        if re.search(input_regex, os.path.basename(root)):
            input_from_path = root

    cover_to_path = input_to_path + "\\CoverIndex"
    if not os.path.exists(cover_to_path):
        os.makedirs(cover_to_path)
    grain_to_path = input_to_path + "\\GrainSize"
    if not os.path.exists(grain_to_path):
        os.makedirs(grain_to_path)
    hydraulics_to_path = input_to_path + "\\Hydraulics"
    if not os.path.exists(hydraulics_to_path):
        os.makedirs(hydraulics_to_path)

    if input_from_path != "None":
        search_and_copy(input_from_path, cover_to_path, r'^(CoverIndex)\.([\w\.]+)$')
        search_and_copy(input_from_path, grain_to_path, r'^(D50)\.([\w\.]+)$')
        search_and_copy(input_from_path, hydraulics_to_path, r'^(Vel)\.([\w\.]+)$')
        search_and_copy(input_from_path, hydraulics_to_path, r'^(Depth)\.([\w\.]+)$')


def get_flow_path(habitat_path):
    dirs = os.listdir(habitat_path)
    flow_path = ''
    if "HydroModelResults" in dirs:
        flow_path = habitat_path + "\\HydroModelResults"
    else:
        for dir in dirs:
            if dir[0] == "S" and dir[1] == "0":
                flow_path = habitat_path + "\\" + dir
    return flow_path


def copy_fis_spawner_data(analyses_to_path, visit_from_path):
    """
    Gets spawner data from Box files and copies it into Riverscapes format
    :param visit_from_path: Where we get our data from
    :param analyses_to_path: Where we put it
    :return: None
    """
    output_from_path = os.path.join(visit_from_path, 'Sims\FIS\Output')
    if not os.path.exists(output_from_path):
        return
    fis_to_path = os.path.join(analyses_to_path, "FIS")
    if not os.path.exists(fis_to_path):
        os.makedirs(fis_to_path)

    chinook_to_path = os.path.join(fis_to_path, "Chinook")
    if not os.path.exists(chinook_to_path):
        os.makedirs(chinook_to_path)
    ch_spawner_to_path = os.path.join(chinook_to_path, "Spawner")
    if not os.path.exists(ch_spawner_to_path):
        os.makedirs(ch_spawner_to_path)
    run_01_ch_to_path = os.path.join(ch_spawner_to_path, "Run_01")
    if not os.path.exists(run_01_ch_to_path):
        os.makedirs(run_01_ch_to_path)

    search_and_copy(output_from_path, run_01_ch_to_path, r'^(FuzzyChinookSpawner_DVSC).(tif)$', "FuzzyHQ")

    steelhead_to_path = os.path.join(fis_to_path, "Steelhead")
    if not os.path.exists(steelhead_to_path):
        os.makedirs(steelhead_to_path)
    st_spawner_to_path = os.path.join(steelhead_to_path, "Spawner")
    if not os.path.exists(st_spawner_to_path):
        os.makedirs(st_spawner_to_path)
    run_01_st_to_path = os.path.join(st_spawner_to_path, "Run_01")
    if not os.path.exists(run_01_st_to_path):
        os.makedirs(run_01_st_to_path)
    search_and_copy(output_from_path, run_01_st_to_path, r'^(FuzzySteelheadSpawner_DVSC).(tif)$', "FuzzyHQ")


def copy_fis_juvenile_hsi_data(analyses_to_path, flow_from_path, row):
    """
    Gets all the other data copied over from Matt's data
    :param analyses_to_path: Where we copy data to
    :param flow_from_path: Where we copy data from
    :param row: The data from the spreadsheet
    :return: None
    """
    simulations_from_path = os.path.join(flow_from_path, "Simulations")
    fis_to_path = os.path.join(analyses_to_path, "FIS")
    if not os.path.exists(fis_to_path):
        os.makedirs(fis_to_path)

    # makes the path to where we want to put the chinook juvenile data. It looks like a lot, but it's really simple code
    chinook_juv_from_path = simulations_from_path + '\\FIS-ch_jv\\Outputs'
    if os.path.exists(chinook_juv_from_path):
        chinook_to_path = os.path.join(fis_to_path, "Chinook")
        if not os.path.exists(chinook_to_path):
            os.makedirs(chinook_to_path)
        ch_juvenile_to_path = os.path.join(chinook_to_path, "Juvenile")
        if not os.path.exists(ch_juvenile_to_path):
            os.makedirs(ch_juvenile_to_path)
        run_01_ch_to_path = os.path.join(ch_juvenile_to_path, "Run_01")
        if not os.path.exists(run_01_ch_to_path):
            os.makedirs(run_01_ch_to_path)

        search_and_copy(chinook_juv_from_path, run_01_ch_to_path, r'^(FIS-ch_jv).(tif)$', "FuzzyHQ")

    # same as above, but for steelhead juveniles
    steelhead_juv_from_path = simulations_from_path + '\\FIS-st_jv\\Outputs'
    if os.path.exists(steelhead_juv_from_path):
        steelhead_to_path = os.path.join(fis_to_path, "Steelhead")
        if not os.path.exists(steelhead_to_path):
            os.makedirs(steelhead_to_path)
        st_juvenile_to_path = os.path.join(steelhead_to_path, "Juvenile")
        if not os.path.exists(st_juvenile_to_path):
            os.makedirs(st_juvenile_to_path)
        run_01_st_to_path = os.path.join(st_juvenile_to_path, "Run_01")
        if not os.path.exists(run_01_st_to_path):
            os.makedirs(run_01_st_to_path)

        search_and_copy(steelhead_juv_from_path, run_01_st_to_path, r'^(FIS-st_jv).(tif)$', "FuzzyHQ")

    hsi_to_path = os.path.join(analyses_to_path, "HSI")
    if not os.path.exists(hsi_to_path):
        os.makedirs(hsi_to_path)

    chinook_juv_from_path = simulations_from_path + '\\HSI-mr_ch_jv_gm\\Outputs'
    if os.path.exists(chinook_juv_from_path):
        chinook_to_path = os.path.join(hsi_to_path, "Chinook")
        if not os.path.exists(chinook_to_path):
            os.makedirs(chinook_to_path)
        ch_juvenile_to_path = os.path.join(chinook_to_path, "Juvenile")
        if not os.path.exists(ch_juvenile_to_path):
            os.makedirs(ch_juvenile_to_path)
        run_01_ch_to_path = os.path.join(ch_juvenile_to_path, "Run_01")
        if not os.path.exists(run_01_ch_to_path):
            os.makedirs(run_01_ch_to_path)

        search_and_copy(chinook_juv_from_path, run_01_ch_to_path, r'^(HSI-mr_ch_jv_gm).(tif)$', "HSI")

    steelhead_juv_from_path = simulations_from_path + '\\HSI-mr_st_jv_gm\\Outputs'
    if os.path.exists(steelhead_juv_from_path):
        steelhead_to_path = os.path.join(hsi_to_path, "Steelhead")
        if not os.path.exists(steelhead_to_path):
            os.makedirs(steelhead_to_path)
        st_juvenile_to_path = os.path.join(steelhead_to_path, "Juvenile")
        if not os.path.exists(st_juvenile_to_path):
            os.makedirs(st_juvenile_to_path)
        run_01_st_to_path = os.path.join(st_juvenile_to_path, "Run_01")
        if not os.path.exists(run_01_st_to_path):
            os.makedirs(run_01_st_to_path)

        search_and_copy(steelhead_juv_from_path, run_01_st_to_path, r'^(HSI-mr_st_jv_gm).(tif)$', "HSI")

    chinook_spawn_from_path = simulations_from_path + '\\HSI-mr_ch_sp_gm\\Outputs'
    if os.path.exists(chinook_spawn_from_path):
        chinook_to_path = os.path.join(hsi_to_path, "Chinook")
        if not os.path.exists(chinook_to_path):
            os.makedirs(chinook_to_path)
        ch_spawner_to_path = os.path.join(chinook_to_path, "Spawner")
        if not os.path.exists(ch_spawner_to_path):
            os.makedirs(ch_spawner_to_path)
        run_01_ch_to_path = os.path.join(ch_spawner_to_path, "Run_01")
        if not os.path.exists(run_01_ch_to_path):
            os.makedirs(run_01_ch_to_path)
        search_and_copy(chinook_spawn_from_path, run_01_ch_to_path, r'^(HSI-mr_ch_sp_gm).(tif)$', "HSI")

    steelhead_spawn_from_path = simulations_from_path + '\\HSI-mr_st_sp_gm\\Outputs'
    if os.path.exists(steelhead_spawn_from_path):
        steelhead_to_path = os.path.join(hsi_to_path, "Steelhead")
        if not os.path.exists(steelhead_to_path):
            os.makedirs(steelhead_to_path)
        st_spawner_to_path = os.path.join(steelhead_to_path, "Spawner")
        if not os.path.exists(st_spawner_to_path):
            os.makedirs(st_spawner_to_path)
        run_01_st_to_path = os.path.join(st_spawner_to_path, "Run_01")
        if not os.path.exists(run_01_st_to_path):
            os.makedirs(run_01_st_to_path)

        search_and_copy(steelhead_spawn_from_path, run_01_st_to_path, r'^(HSI-mr_st_sp_gm).(tif)$', "HSI")

    # copies in
    global fis_model_path
    if row.avg_bfw_val > 10:
        sites_path = os.path.join(fis_model_path, "LargeSites")
    else:
        sites_path = os.path.join(fis_model_path, "SmallSites")

    fis_steelhead_spawner_run01_path = fis_to_path + '\\Steelhead\Spawner\Run_01\FISModel'
    if not os.path.exists(fis_steelhead_spawner_run01_path):
        os.makedirs(fis_steelhead_spawner_run01_path)
    search_and_copy(sites_path, fis_steelhead_spawner_run01_path, r"^FuzzySteelheadSpawner_DVSC.fis$")

    fis_chinook_spawner_run01_path = fis_to_path + '\\Chinook\Spawner\Run_01\FISModel'
    if not os.path.exists(fis_chinook_spawner_run01_path):
        os.makedirs(fis_chinook_spawner_run01_path)
    search_and_copy(sites_path, fis_chinook_spawner_run01_path, r"^FuzzyChinookSpawner_DVSC.fis$")

    fis_chinook_juvenile_run01_path = fis_to_path + '\\Chinook\Juvenile\Run_01\FISModel'
    if not os.path.exists(fis_chinook_juvenile_run01_path):
        os.makedirs(fis_chinook_juvenile_run01_path)
    search_and_copy(sites_path, fis_chinook_juvenile_run01_path, r"^FuzzyChinookJuvenile_DVSC.fis$")

    fis_steelhead_juvenile_run01_path = fis_to_path + '\\Steelhead\Juvenile\Run_01\FISModel'
    if not os.path.exists(fis_steelhead_juvenile_run01_path):
        os.makedirs(fis_steelhead_juvenile_run01_path)
    search_and_copy(sites_path, fis_steelhead_juvenile_run01_path, r"^FuzzySteelheadJuvenile_DVSC.fis$")


def set_up_analyses(visit_from_path, visit_to_path, row):
    """
    Sets up the analyses folder
    :param visit_from_path: Where we get FIS spawner data
    :param visit_to_path: The folder that we want to copy our data to
    :param row: Contains the data to get us to where analyses data is held
    :return: None
    """
    analyses_to_path = visit_to_path + "\\Analyses"
    if not os.path.exists(analyses_to_path):
        os.makedirs(analyses_to_path)

    copy_fis_spawner_data(analyses_to_path, visit_from_path)

    global analyses_from_path
    habitat_from_path = analyses_from_path + '\\' + row.year + '\\' + row.watershed + '\\' + row.site_name + '\\VISIT_' + row.visit_id + '\\Habitat'
    flow_from_path = get_flow_path(habitat_from_path)

    if not flow_from_path:
        return

    copy_fis_juvenile_hsi_data(analyses_to_path, flow_from_path, row)


def find_row(target_visit, row_list):
    """
    Finds the row that has the data for the target visit
    :param target_visit: The visit whose data we want to find
    :param row_list: The rows of the csv file we have, parsed into a list
    :return: Either the proper row, or False
    """
    for row in row_list:
        if target_visit == row.visit_id:
            return row
    return False


def set_up_visits(site_from_path, site_to_path, row_list):
    """
    Sets up the visits that we will copy data into
    :param site_from_path: The site that we want to copy data from
    :param site_to_path: The site that we want to copy data to
    :return: NULL
    """
    for visit_dir in os.listdir(site_from_path):
        target_visit = visit_dir[6:-1] + visit_dir[-1]
        row = find_row(target_visit, row_list)
        if row:
            visit_from_path = site_from_path + "\\" + visit_dir
            visit_to_path = site_to_path + "\\" + visit_dir
            if not os.path.exists(visit_to_path):
                os.makedirs(visit_to_path)

            visit_to_path += '\\S000' + row.flow
            if not os.path.exists(visit_to_path):
                os.makedirs(visit_to_path)

            set_up_inputs(visit_to_path, visit_from_path)
            set_up_analyses(visit_from_path, visit_to_path, row)


def set_up_sites(from_path, to_path, year, row_list):
    """
    Copies data from our sites to our new
    :param from_path: The path that we want to copy data from, ending with the Watershed
    :param to_path: The path that we want to copy data to, ending with the Watershed
    :param year: The year which we're copying data from
    :return: NULL
    """
    for site_dir in os.listdir(from_path):
        site_to_path = to_path + "\\" + site_dir
        year_to_path = site_to_path + "\\" + year
        site_from_path = from_path + "\\" + site_dir

        if not os.path.exists(site_to_path):
            os.makedirs(site_to_path)
        if not os.path.exists(year_to_path):
            os.makedirs(year_to_path)
        set_up_visits(site_from_path, year_to_path, row_list)


def copy_to_riverscapes_format(from_path, to_path, row_list):
    """
    Copies over data from a certain year to our Riverscapes format
    :param from_path: The path that we want to copy data from, ending with the Watershed
    :param to_path: The path that we want to copy data to, ending with the Watershed
    :return: NULL
    """
    if not os.path.exists(from_path):
        return

    year = os.path.basename(os.path.normpath(dirname(from_path)))  # gets the year from the file path

    set_up_sites(from_path, to_path, year, row_list)


def copy_region(region, row_list):
    to_path = "C:\Users\A02150284\Documents\NewFHMData\\" + region
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    for i in range(2012, 2017):
        print "Copying over " + str(i) + " data from the " + region
        copy_to_riverscapes_format("C:\Users\A02150284\Documents\FHMData\\" + str(i) + "\\" + region,
                                   to_path, row_list)


def clean_up(root):
    for dir in os.listdir(root):
        if os.path.isdir(root + '\\' + dir):
            clean_up(root + '\\' + dir)
    if os.listdir(root) == []:
        os.rmdir(root)


def main():
    if not os.path.exists("C:\Users\A02150284\Documents\NewFHMData"):
        os.makedirs("C:\Users\A02150284\Documents\NewFHMData")

    row_list = []
    counter = 0
    with open('visits_with_discharge.txt', 'r') as file:
        for line in file.readlines():
            counter += 1
            match = re.match(r'^([\w\d\s]+),([\w\d\s\-]+),([\d]+),([\d]+),([\d\.]+),([\w]+),([\d\.]+)$', line)
            if match:
                data = match.groups()
                flow = ''
                for i in range(0, len(data[4])):
                    if data[4][i] == '.':
                        flow += '_'
                    else:
                        flow += data[4][i]
                row_list.append(FlowRowObject(data[0], data[1], data[2], data[3], flow, data[5], data[6]))

    copy_region("Asotin", row_list)
    copy_region("Entiat", row_list)
    copy_region("JohnDay", row_list)
    copy_region("Lemhi", row_list)
    copy_region("Methow", row_list)
    copy_region("Minam", row_list)
    copy_region("Region17", row_list)
    copy_region("SouthForkSalmon", row_list)
    copy_region("Tucannon", row_list)
    copy_region("UpperGrandeRonde", row_list)
    copy_region("WallaWalla", row_list)
    copy_region("Wenatchee", row_list)
    copy_region("YankeeFork", row_list)

    clean_up("C:\Users\A02150284\Documents\NewFHMData")


if __name__ == "__main__":
    main()

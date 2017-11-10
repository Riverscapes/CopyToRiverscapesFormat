class FlowRowObject:
    def __init__(self, watershed, site_name, year, visit_id, flow, has_HSI_data, avg_bfw_val):
        self.watershed = watershed
        self.watershed = self.watershed.replace(" ", "")
        self.site_name = site_name
        self.site_name = self.site_name.replace(" ", "")
        self.year = year
        self.visit_id = visit_id
        self.flow = flow
        if has_HSI_data == "Yes":
            self.has_HSI_data = True
        elif has_HSI_data == "No":
            self.has_HSI_data = False
        elif has_HSI_data == "Maybe":
            self.has_HSI_data = False
        else:
            raise Exception("invalid has_HSI_data value passed: " + str(has_HSI_data))
        self.avg_bfw_val = float(avg_bfw_val)

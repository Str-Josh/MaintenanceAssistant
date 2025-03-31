
from mymodels import db, Asset
from datetime import date

# A device that is under "Maintenance".
class MaintenanceDevice:
    def __init__(self):
        return None


# Given 200 AED units
xray_install_date = "01/01/2025"
xray_units_available = 200
xray_data = [
    {
        "date": "02/02/2025",
        "units": 85,
        "mode": "Radiation sensor failure",
        "downtime": 45,
        "recovery": 30
    },
    {
        "date": "03/06/2025",
        "units": 120,
        "mode": "Radiation sensor failure",
        "downtime": 60,
        "recovery": 38
    }
]

def kaplan_meier_estimator_function(total_units, failure_data):
    # assume failure_data is list[dict] s.t. dict["date", "units"]
    survival_curve = []

    installation_date = xray_install_date
    last_failure_date = failure_data[-1]["date"]
    
    if type(installation_date) is str:  # assume both are same
        installation_decomp = installation_date.split("/")
        last_failure_date_decomp = last_failure_date.split("/")

        installation_month = installation_decomp[0]
        installation_day = installation_decomp[1]
        installation_year = installation_decomp[2]

        last_failure_month = installation_decomp[0]
        last_failure_day = installation_decomp[1]
        last_failure_year = installation_decomp[2]

        installation_date = date(installation_year, installation_month, installation_day)
        last_failure_date = date(last_failure_year, last_failure_month, last_failure_day)
    
    delta = last_failure_date - installation_date
    age_at_last_failure = delta.days

    prod = 1
    for failure_datum in failure_data:
        past_dates = []
        if failure_datum["date"] in past_dates:
            prev_calc = survival_curve[-1]
            # Come back later cuz I'm tired atm
            pass

        if type(failure_datum["date"]) is str:
            failure_datum_date_decomp = failure_datum["date"].split("/")
            failure_datum_date_month = failure_datum_date_decomp[0]
            failure_datum_date_day = failure_datum_date_decomp[1]
            failure_datum_date_year = failure_datum_date_decomp[2]
            
            failure_datum_date = date(
                failure_datum_date_year,
                failure_datum_date_month,
                failure_datum_date_day
            )
        failure_age_delta = failure_datum_date - installation_date
        age_at_this_failure = failure_age_delta.days

        prod *= (1 - (failure_data["units"] / total_units))
        if prod < 0:
            raise ValueError("There was an error in the data.")
        survival_curve.append(prod)
    return survival_curve


class PredictionModel:
    def __init__(self, asset_id):
        self.asset = Asset.query.filter_by(asset_id = asset_id).first()
        return None
    
    def identify_model(self, failure_):
        # if failure_history.contains(years > 3)
        pass
from math import floor

class StochasticGammaProcess_FiniteTimePolicy():
    def __init__(self):
        self.delta = None

        self.critical_threshold = None
        self.degradation_threshold = None

        self.inspection_cost = None
        self.preventive_maintenance_cost = None
        self.failure_cost = None

        # self.total_cost_renewal_cycle = floor(time / delta) * self.inspection_cost + self.preventive_maintenance_cost
        self.total_cost_renewal_cycle = None
    
        pass

    def failure_event_announcement(self, inspection_degradation):
        if inspection_degradation > self.degradation_threshold and inspection_degradation < self.critical_threshold:
            time = 4  # change later
            self.commence_preventive_maintenance(time)
            pass

    def commence_preventive_maintenance(self, current_time):
        from math import floor
        self.total_cost_renewal_cycle = floor(current_time / self.delta) * self.inspection_cost + self.preventive_maintenance_cost

    def commence_corrective_maintenance(self, current_time):
        self.total_cost_renewal_cycle = floor(current_time / self.delta) * self.inspection_cost + self.failure_cost

    def identify_best_model(degradation:list):
        classifications = ["BN", "SGP", "HMM"]
        
        degradation_rate_determination = []
        for i in range(len(degradation)):
            if i == 0:
                continue
            if degradation[i] > degradation[i-1]:
                degradation_rate_determination.append("increasing")
        if "decreasing" in degradation:
            return classifications[2]
        

        
        return None



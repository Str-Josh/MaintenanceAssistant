import datetime as dt

mock_users = [
    {
        "username": "demo", 
        "first_name": "demo",
        "last_name": "demo",
        "user_role": "admin",
        "email": "demo@gmail.com",
        "password": "demo"
    },
    {
        "username": "director", 
        "first_name": "director",
        "last_name": "director",
        "user_role": "director", 
        "email": "director@gmail.com",
        "password": "director"
    },
    {
        "username": "staff", 
        "first_name": "staff",
        "last_name": "staff",
        "user_role": "staff",
        "email": "staff@gmail.com",
        "password": "staff"
    },
    {
        "username": "abbyburton", 
        "first_name": "Abby",
        "last_name": "Burton",
        "user_role": "director", 
        "email": "abbyburton@gmail.com",
        "password": "abbyburton"
    },
    {
        "username": "john", 
        "first_name": "John",
        "last_name": "Doe",
        "user_role": "manager", 
        "email": "john@gmail.com",
        "password": "john"
    },
    {
        "username": "mary", 
        "first_name": "Mary",
        "last_name": "Strawberry",
        "user_role": "manager", 
        "email": "mary@gmail.com",
        "password": "mary"
    },
    {
        "username": "zachwalter", 
        "first_name": "Zach",
        "last_name": "Walter",
        "user_role": "manager", 
        "email": "zachwalter@gmail.com",
        "password": "zachwalter"
    },

    {
        "username": "marsolis", 
        "first_name": "Marjorie",
        "last_name": "Solis",
        "user_role": "manager", 
        "email": "marsolis@gmail.com",
        "password": "marsolis"
    },
    {
        "username": "markhebert", 
        "first_name": "Mark",
        "last_name": "Hebert",
        "user_role": "manager", 
        "email": "markhebert@gmail.com",
        "password": "markhebert"
    },

    {
        "username": "jandrews", 
        "first_name": "James",
        "last_name": "Andrews",
        "user_role": "staff", 
        "email": "jandrews@gmail.com",
        "password": "jandrews"
    },
    {
        "username": "jgriffith", 
        "first_name": "Jason",
        "last_name": "Griffith",
        "user_role": "staff", 
        "email": "jgriffith@gmail.com",
        "password": "jgriffith"
    },
    {
        "username": "crussell", 
        "first_name": "Cameron",
        "last_name": "Russell",
        "user_role": "staff",
        "email": "crussell@gmail.com",
        "password": "crussell"
    },
]

mock_notifications = [
    {
        "sender": "demo",
        "recipient": "john",
        "notification_send_date": dt.date.today() - dt.timedelta(days=1),
        "notification_head": "Help! AED is flashing red light", 
        "notification_body": "AED was being used for ... and when I ... the AED ...",
    },
    {
        "sender": "demo",
        "recipient": "mary",
        "notification_send_date": dt.date.today() - dt.timedelta(days=1),
        "notification_head": "Help! AED is flashing red light", 
        "notification_body": "AED was being used for ... and when I ... the AED ...",
    },
    {
        "sender": "demo",
        "recipient": "zachwalter",
        "notification_send_date": dt.date.today() - dt.timedelta(days=1),
        "notification_head": "Help! AED is flashing red light", 
        "notification_body": "AED was being used for ... and when I ... the AED ...",
    },
    {
        "sender": "demo",
        "recipient": "marsolis",
        "notification_send_date": dt.date.today() - dt.timedelta(days=1),
        "notification_head": "Help! AED is flashing red light", 
        "notification_body": "AED was being used for ... and when I ... the AED ...",
    },
    {
        "sender": "demo",
        "recipient": "markhebert",
        "notification_send_date": dt.date.today() - dt.timedelta(days=1),
        "notification_head": "Help! AED is flashing red light", 
        "notification_body": "AED was being used for ... and when I ... the AED ...",
    },
    {
        "sender": "Nurse Magda",
        "recipient": "john",
        "notification_send_date": dt.date.today() - dt.timedelta(days=2),
        "notification_head": "X-ray scanner is making a weird noise", 
        "notification_body": "When working with a patient, the scanner started making a deep grumble sound.",
    },
]

mock_assets = [
    {
        "asset_id": 1,
        "serial_number": "0001",
        "asset_name": "CardiGuard 3000",
        "brand": "HeartSafe",
        "generic_name": "Automated External Defibrillator (AED)",
        "manufacturer": "",
        "location": "",
        "average_use_per_year": "500 uses",
        "total_units_in_service": 20000,
        "failure_incidents_in_past_year": 50,
        "total_failures_in_history": 200,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 150,
        "maintenance_type": "Battery replacement and calibration",
        "cost_per_maintenance_activity": 50.00,
        "total_maintenance_costs_in_past_year": 7500.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=2),
    },
    {
        "asset_id": 2,
        "serial_number": "0010",
        "asset_name": "BioVent Pro",
        "brand": "AirHealth",
        "generic_name": "Mechanical Ventilator",
        "manufacturer": "RespiraTech Ltd.",
        "location": "",
        "average_use_per_year": "100000 hours",
        "total_units_in_service": 5000,
        "failure_incidents_in_past_year": 15,
        "total_failures_in_history": 80,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 300,
        "maintenance_type": "Circuit board inspection and cleaning",
        "cost_per_maintenance_activity": 120.00,
        "total_maintenance_costs_in_past_year": 36000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=4),
    },
    {
        "asset_id": 3,
        "serial_number": "0011",
        "asset_name": "SafePulse Infusion Pump",
        "brand": "MedFusion",
        "generic_name": "Infusion Pump",
        "manufacturer": "HealthTech Innovations",
        "location": "",
        "average_use_per_year": "50000 hours",
        "total_units_in_service": 10000,
        "failure_incidents_in_past_year": 40,
        "total_failures_in_history": 250,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 500,
        "maintenance_type": "Pump motor inspection and replacement",
        "cost_per_maintenance_activity": 200.00,
        "total_maintenance_costs_in_past_year": 100000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=5),
    },
    {
        "asset_id": 4,
        "serial_number": "0100",
        "asset_name": "MediScope 4K",
        "brand": "ScopeVision",
        "generic_name": "Endoscope",
        "manufacturer": "MediScope Technologies",
        "location": "",
        "average_use_per_year": "200 uses",
        "total_units_in_service": 12000,
        "failure_incidents_in_past_year": 90,
        "total_failures_in_history": 350,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 600,
        "maintenance_type": "Lens cleaning and inspection",
        "cost_per_maintenance_activity": 75.00,
        "total_maintenance_costs_in_past_year": 45000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=8),
    },
    {
        "asset_id": 5,
        "serial_number": "0101",
        "asset_name": "GlucoTrack 1000",
        "brand": "HealthGlobe",
        "generic_name": "Continuous Glucose Monitor (CGM)",
        "manufacturer": "Diabetech Industries",
        "location": "Emergeny",
        "average_use_per_year": "300000 sensor readings",
        "total_units_in_service": 50000,
        "failure_incidents_in_past_year": 1000,
        "total_failures_in_history": 2500,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 1200,
        "maintenance_type": "Sensor replacement and calibration",
        "cost_per_maintenance_activity": 30.00,
        "total_maintenance_costs_in_past_year": 36000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=12),
    },
    {
        "asset_id": 6,
        "serial_number": "0110",
        "asset_name": "NeoPulse ECG Monitor",
        "brand": "PulseMed",
        "generic_name": "Electrocardiogram (ECG)",
        "manufacturer": "CardioCare Solutions",
        "location": "",
        "average_use_per_year": "75000 hours",
        "total_units_in_service": 25000,
        "failure_incidents_in_past_year": 175,
        "total_failures_in_history": 1000,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 500,
        "maintenance_type": "Lead inspection and cleaning",
        "cost_per_maintenance_activity": 50.00,
        "total_maintenance_costs_in_past_year": 25000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=13),
    },
    {
        "asset_id": 7,
        "serial_number": "0111",
        "asset_name": "SurgiLaser Pro",
        "brand": "LaserTech",
        "generic_name": "Laser Surgical System",
        "manufacturer": "OptiSurgical Inc.",
        "location": "",
        "average_use_per_year": "1000 hours",
        "total_units_in_service": 3000,
        "failure_incidents_in_past_year": 30,
        "total_failures_in_history": 150,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 100,
        "maintenance_type": "Laser calibration and alignment",
        "cost_per_maintenance_activity": 500.00,
        "total_maintenance_costs_in_past_year": 50000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=6),
    },
    {
        "asset_id": 8,
        "serial_number": "1000",
        "asset_name": "DermalScan X-ray",
        "brand": "DermTech",
        "generic_name": "X-ray Imaging System",
        "manufacturer": "RadMed Industries",
        "location": "",
        "average_use_per_year": "50000 images",
        "total_units_in_service": 2000,
        "failure_incidents_in_past_year": 18,
        "total_failures_in_history": 100,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 150,
        "maintenance_type": "Radiation sensor inspection and recalibration",
        "cost_per_maintenance_activity": 150.00,
        "total_maintenance_costs_in_past_year": 22500.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=14),
    },
    {
        "asset_id": 9,
        "serial_number": "1001",
        "asset_name": "NephroClean Dialysis Machine",
        "brand": "LifePure",
        "generic_name": "Hemodialysis Machine",
        "manufacturer": "NephroCare Medical",
        "location": "",
        "average_use_per_year": "40000 dialysis sessions",
        "total_units_in_service": 8000,
        "failure_incidents_in_past_year": 112,
        "total_failures_in_history": 400,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 1000,
        "maintenance_type": "Fluid pump inspection and replacement",
        "cost_per_maintenance_activity": 300.00,
        "total_maintenance_costs_in_past_year": 300000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=22),
    },
    {
        "asset_id": 10,
        "serial_number": "1010",
        "asset_name": "VisionPlus Retinal Scanner",
        "brand": "EyeTech",
        "generic_name": "Optical Coherence Tomography (OCT) Scanner",
        "manufacturer": "Visionary Medical Devices",
        "location": "",
        "average_use_per_year": "25000 scans",
        "total_units_in_service": 3500,
        "failure_incidents_in_past_year": 21,
        "total_failures_in_history": 150,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 180,
        "maintenance_type": "Sensor recalibration and lens cleaning",
        "cost_per_maintenance_activity": 250.00,
        "total_maintenance_costs_in_past_year": 45000.00,
        "upcoming_maintenance_action_date": dt.date.today() + dt.timedelta(days=17),
    },
]

mock_activities = [
    {
        "description": "Monthly inspection of HVAC system",
        "type": "Inspection",
        "frequency": "Monthly",
        "date": dt.date(2025, 4, 15),
        "time": dt.time(9, 0)
    },
    {
        "description": "Quarterly safety drill",
        "type": "Drill",
        "frequency": "Quarterly",
        "date": dt.date(2025, 3, 10),
        "time": dt.time(14, 30)
    },
    {
        "description": "Software update on workstations",
        "type": "Maintenance",
        "frequency": "Bi-annually",
        "date": dt.date(2025, 4, 5),
        "time": dt.time(10, 0)
    },
    {
        "description": "Annual fire extinguisher check",
        "type": "Inspection",
        "frequency": "Annually",
        "date": dt.date(2025, 1, 20),
        "time": dt.time(11, 0)
    },
    {
        "description": "Weekly cleaning of lab equipment",
        "type": "Cleaning",
        "frequency": "Weekly",
        "date": dt.date(2025, 4, 17),
        "time": dt.time(8, 30)
    }
]

mock_activitiesUsers = [
    {
        "user_id": 1,
        "activity_id": 1,
        "asset_id": "ASSET001",
        "date": dt.date(2025, 4, 15),
        "time": dt.time(9, 0),
        "notes": "System was functioning normally. No issues found."
    },
    {
        "user_id": 2,
        "activity_id": 2,
        "asset_id": "ASSET002",
        "date": dt.date(2025, 3, 10),
        "time": dt.time(14, 30),
        "notes": "All staff participated in the drill. Timed at 5 minutes."
    },
    {
        "user_id": 1,
        "activity_id": 3,
        "asset_id": "ASSET003",
        "date": dt.date(2025, 4, 5),
        "time": dt.time(10, 0),
        "notes": "Software updated to version 4.5.1"
    },
    {
        "user_id": 3,
        "activity_id": 4,
        "asset_id": "ASSET001",
        "date": dt.date(2025, 1, 20),
        "time": dt.time(11, 0),
        "notes": "All extinguishers were fully charged and tagged."
    },
    {
        "user_id": 2,
        "activity_id": 5,
        "asset_id": "ASSET002",
        "date": dt.date(2025, 4, 17),
        "time": dt.time(8, 30),
        "notes": "Standard weekly cleaning completed without incident."
    }
]





"""
    {
        "asset_name": "",
        "brand": "",
        "generic_name": "",
        "manufacturer": "",
        "location": "",
        "average_use_per_year": "",
        "total_units_in_service": 0,
        "failure_incidents_in_past_year": 0,
        "total_failures_in_history": 0,
        "last_maintenance_date": dt.date(2025, 1, 1),
        "total_maintenance_activities_in_past_year": 0,
        "maintenance_type": "",
        "cost_per_maintenance_activity": 0.00,
        "total_maintenance_costs_in_past_year": 0.00,
    },
"""
# Amendment history data structure

# Store amendment history for each act, section, and specialized tribunal
amendment_history = {
    # Specialized Tribunals in Himachal Pradesh
    "HP_Tribunals": {
        "Administrative_Tribunal": [
            {
                "implementation_date": "2024-01-15",
                "old_text": "Previous jurisdiction over service matters",
                "new_text": "Enhanced jurisdiction including contractual employees",
                "amendment_act": "HP Administrative Tribunal (Amendment) Act, 2024",
                "summary": "Extended jurisdiction to cover contractual employees in service matters"
            }
        ],
        "Consumer_Forums": {
            "State": [
                {
                    "implementation_date": "2024-02-01",
                    "old_text": "Monetary limit up to Rs. 1 crore",
                    "new_text": "Monetary limit enhanced to Rs. 2 crores",
                    "amendment_act": "Consumer Protection (HP Amendment) Rules, 2024",
                    "summary": "Increased monetary jurisdiction of State Consumer Forum"
                }
            ],
            "District": [
                {
                    "implementation_date": "2024-02-01",
                    "old_text": "Monetary limit up to Rs. 20 lakhs",
                    "new_text": "Monetary limit enhanced to Rs. 50 lakhs",
                    "amendment_act": "Consumer Protection (HP Amendment) Rules, 2024",
                    "summary": "Increased monetary jurisdiction of District Consumer Forums"
                }
            ]
        },
        "Labour_Courts": [
            {
                "implementation_date": "2024-03-01",
                "old_text": "Previous provisions for industrial disputes",
                "new_text": "Updated provisions including gig workers",
                "amendment_act": "HP Industrial Relations Code, 2024",
                "summary": "Extended protection to gig economy workers"
            }
        ],
        "Family_Courts": [
            {
                "implementation_date": "2024-01-20",
                "old_text": "Previous mediation procedures",
                "new_text": "Mandatory pre-litigation mediation in family disputes",
                "amendment_act": "HP Family Courts (Amendment) Rules, 2024",
                "summary": "Introduction of mandatory mediation before filing family disputes"
            }
        ],
        "Lok_Adalats": [
            {
                "implementation_date": "2024-02-15",
                "old_text": "Quarterly Lok Adalat schedule",
                "new_text": "Monthly Lok Adalat schedule with specialized benches",
                "amendment_act": "HP Legal Services Authority Rules, 2024",
                "summary": "Increased frequency and specialization of Lok Adalats"
            }
        ],
        "State_Information_Commission": [
            {
                "implementation_date": "2024-03-10",
                "old_text": "Previous appeal procedures",
                "new_text": "Online filing of RTI appeals and complaints",
                "amendment_act": "HP Right to Information Rules, 2024",
                "summary": "Digitalization of RTI appeal process"
            }
        ],
        "Forest_Settlement_Courts": [
            {
                "implementation_date": "2024-02-28",
                "old_text": "Previous forest rights settlement process",
                "new_text": "Streamlined process with digital documentation",
                "amendment_act": "HP Forest Rights Rules, 2024",
                "summary": "Modernization of forest rights settlement procedures"
            }
        ]
    },
    "IPC": {
        "354A": [
            {
                "implementation_date": "2013-04-02",
                "old_text": "Previous version of section dealing with sexual harassment",
                "new_text": "Sexual harassment and punishment for sexual harassment",
                "amendment_act": "Criminal Law (Amendment) Act, 2013",
                "summary": "Added specific definitions and punishments for sexual harassment"
            }
        ],
        "376": [
            {
                "implementation_date": "2013-04-02",
                "old_text": "Previous rape law provisions",
                "new_text": "Expanded definition and stricter punishment for rape",
                "amendment_act": "Criminal Law (Amendment) Act, 2013",
                "summary": "Comprehensive changes to rape laws following the 2012 Delhi gang rape case"
            },
            {
                "implementation_date": "2018-08-11",
                "old_text": "Minimum 7 years imprisonment",
                "new_text": "Minimum 10 years imprisonment",
                "amendment_act": "Criminal Law (Amendment) Act, 2018",
                "summary": "Enhanced minimum punishment for rape of women"
            },
            {
                "implementation_date": "2024-02-15",
                "old_text": "Previous provisions for investigation timeline",
                "new_text": "Mandatory completion of investigation within 60 days",
                "amendment_act": "Criminal Law (Amendment) Act, 2024",
                "summary": "Introduced strict timeline for investigation completion in rape cases"
            }
        ],
        "498A": [
            {
                "implementation_date": "2024-01-10",
                "old_text": "Previous provisions for cruelty against women",
                "new_text": "Enhanced provisions with specific categories of mental and physical cruelty",
                "amendment_act": "Protection of Women (Criminal Law Amendment) Act, 2024",
                "summary": "Expanded definition of cruelty and introduced stricter penalties"
            }
        ]
    },
    "IT Act": {
        "66A": [
            {
                "implementation_date": "2015-03-24",
                "old_text": "Punishment for sending offensive messages through communication services",
                "new_text": "Section struck down as unconstitutional",
                "amendment_act": "Supreme Court judgment in Shreya Singhal v. Union of India",
                "summary": "Section declared unconstitutional for violating freedom of speech"
            }
        ],
        "67A": [
            {
                "implementation_date": "2024-03-01",
                "old_text": "Previous provisions for publishing sexually explicit content",
                "new_text": "Enhanced penalties and inclusion of AI-generated explicit content",
                "amendment_act": "Information Technology (Amendment) Act, 2024",
                "summary": "Updated provisions to address AI-generated explicit content and increased penalties"
            }
        ]
    },
    "CrPC": {
        "161": [
            {
                "implementation_date": "2024-02-20",
                "old_text": "Previous provisions for recording statements",
                "new_text": "Mandatory video recording of witness statements",
                "amendment_act": "Criminal Procedure (Amendment) Act, 2024",
                "summary": "Introduction of mandatory video recording for witness statements"
            }
        ]
    }
}

def get_recent_amendments(days=90):
    """Get list of sections amended within specified number of days"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    
    recent_amendments = []
    for act, sections in amendment_history.items():
        if act == 'HP_Tribunals':
            # Handle specialized tribunals structure
            for tribunal, tribunal_data in sections.items():
                if isinstance(tribunal_data, list):
                    # Handle direct list of amendments
                    for amendment in tribunal_data:
                        amendment_date = datetime.strptime(amendment['implementation_date'], '%Y-%m-%d')
                        if amendment_date >= cutoff_date:
                            recent_amendments.append({
                                'act': act,
                                'section': tribunal,
                                'implementation_date': amendment['implementation_date'],
                                'summary': amendment['summary']
                            })
                elif isinstance(tribunal_data, dict):
                    # Handle nested structure (e.g., Consumer_Forums)
                    for sub_section, amendments in tribunal_data.items():
                        for amendment in amendments:
                            amendment_date = datetime.strptime(amendment['implementation_date'], '%Y-%m-%d')
                            if amendment_date >= cutoff_date:
                                recent_amendments.append({
                                    'act': act,
                                    'section': f"{tribunal}/{sub_section}",
                                    'implementation_date': amendment['implementation_date'],
                                    'summary': amendment['summary']
                                })
        else:
            # Handle regular amendments structure
            for section, amendments in sections.items():
                for amendment in amendments:
                    amendment_date = datetime.strptime(amendment['implementation_date'], '%Y-%m-%d')
                    if amendment_date >= cutoff_date:
                        recent_amendments.append({
                            'act': act,
                            'section': section,
                            'implementation_date': amendment['implementation_date'],
                            'summary': amendment['summary']
                        })

    
    return sorted(recent_amendments, key=lambda x: x['implementation_date'], reverse=True)

def get_amendment_history(act, section):
    """Get complete amendment history for a specific section"""
    return amendment_history.get(act, {}).get(section, [])

def get_latest_amendment(act, section):
    """Get the most recent amendment for a specific section"""
    history = get_amendment_history(act, section)
    if history:
        return max(history, key=lambda x: x['implementation_date'])
    return None
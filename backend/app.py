from flask import Flask, jsonify, request
from pymongo import MongoClient
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)


client = MongoClient("mongodb://localhost:27017/")
db = client["dummy"]
references_collection = db["reference"]
papers_collection = db["paper"]
paper_data_collection = db["paperData"]
author_collection = db["auth"]
affiliation_collection = db["aff"]
author_affiliation_collection = db["authaff"]

def cl2l3(cited):
    cited2=[]
    seen_paper_ids = set()  
    for cite in cited:
            if cite["PaperID"] not in seen_paper_ids:
                papers_cited = references_collection.find({"Cited_PaperID": cite["PaperID"]}, {"Citing_PaperID": 1, "_id": 0})
                for cited_paper in papers_cited:
                    citing_paper_id = cited_paper["Citing_PaperID"]
                    citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1})
                    if citing_paper_info:
                        paper_id = citing_paper_id
                        year = citing_paper_info.get("Year")
                        cited2.append({
                            "Main":cite["PaperID"],
                            "PaperID": paper_id,
                            "Year": year,
                            "Name":paper_data_collection.find_one({"PaperID": paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
                        })
                seen_paper_ids.add(cite["PaperID"])
                
    return cited2

def rl2l3(referenced_by):
    referenced_by2 = []  
    seen_paper_ids = set()  
    for refer in referenced_by:
        if refer["Main"] not in seen_paper_ids:
            papers_referenced = references_collection.find({"Citing_PaperID": refer["Main"]}, {"Cited_PaperID": 1, "_id": 0})
            for referenced_paper in papers_referenced:
                referenced_paper_id = referenced_paper["Cited_PaperID"]
                referenced_paper_info = db["paper"].find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1})
                if referenced_paper_info:
                    referenced_by2.append({
                        "Main":referenced_paper_id,
                        "PaperID": refer["Main"],
                        "Year": referenced_paper_info.get("Year"),
                        "Name":paper_data_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
                    })
            seen_paper_ids.add(refer["Main"])

    return referenced_by2


@app.route('/paper/testl1/<string:paper_id>', methods=['GET'])
def get_paper_citation(paper_id):

    cited = []
    referenced_by = []

    data={}

    papers_cited = references_collection.find({"Cited_PaperID": paper_id}, {"Citing_PaperID": 1, "_id": 0})
    for cited_paper in papers_cited:
        citing_paper_id = cited_paper["Citing_PaperID"]
        citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1})
        if citing_paper_info:
            cited.append({
                "Main":paper_id,
                "PaperID": citing_paper_id,
                "Year": citing_paper_info.get("Year"),
                "Name":paper_data_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })
    
    papers_referenced = references_collection.find({"Citing_PaperID": paper_id}, {"Cited_PaperID": 1, "_id": 0})
    for referenced_paper in papers_referenced:
        referenced_paper_id = referenced_paper["Cited_PaperID"]
        referenced_paper_info = db["paper"].find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1})
        if referenced_paper_info:
            referenced_by.append({
                "Main":referenced_paper_id,
                "PaperID": paper_id,
                "Year": referenced_paper_info.get("Year"),
                "Name":paper_data_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })
    
    cited2=cl2l3(cited)
    cited3=cl2l3(cited2)
    referenced_by2=rl2l3(referenced_by)
    referenced_by3=rl2l3(referenced_by2)

    data={
        "Paper":paper_id,
        "Year":papers_collection.find_one({"PaperID": paper_id}, {"_id": 0, "Year": 1}).get("Year"),
        "Name":paper_data_collection.find_one({"PaperID": paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
        "Citeref":[]
    }

    for i in cited:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in referenced_by:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in cited2:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in cited3:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in referenced_by2:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in referenced_by3:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    

    return jsonify(data)

@app.route('/paper/refer/<string:paper_id>', methods=['GET'])
def get_paper_refer(paper_id):

    referenced_by = []

    data={}

    papers_referenced = references_collection.find({"Citing_PaperID": paper_id}, {"Cited_PaperID": 1, "_id": 0})
    for referenced_paper in papers_referenced:
        referenced_paper_id = referenced_paper["Cited_PaperID"]
        referenced_paper_info = db["paper"].find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1})
        if referenced_paper_info:
            referenced_by.append({
                "Main":referenced_paper_id,
                "PaperID": paper_id,
                "Year": referenced_paper_info.get("Year"),
                "Name":paper_data_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })
    
    referenced_by2=rl2l3(referenced_by)
    referenced_by3=rl2l3(referenced_by2)

    data={
        "Paper":paper_id,
        "Year":papers_collection.find_one({"PaperID": paper_id}, {"_id": 0, "Year": 1}).get("Year"),
        "Name":paper_data_collection.find_one({"PaperID": paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
        "Citeref":[]
    }

    for i in referenced_by:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in referenced_by2:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in referenced_by3:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    

    return jsonify(data)

@app.route('/paper/cite/<string:paper_id>', methods=['GET'])
def cite(paper_id):

    cited = []
    data={}

    papers_cited = references_collection.find({"Cited_PaperID": paper_id}, {"Citing_PaperID": 1, "_id": 0})
    for cited_paper in papers_cited:
        citing_paper_id = cited_paper["Citing_PaperID"]
        citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1})
        if citing_paper_info:
            cited.append({
                "Main":paper_id,
                "PaperID": citing_paper_id,
                "Year": citing_paper_info.get("Year"),
                "Name":paper_data_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })
    
    
    cited2=cl2l3(cited)
    cited3=cl2l3(cited2)

    data={
        "Paper":paper_id,
        "Year":papers_collection.find_one({"PaperID": paper_id}, {"_id": 0, "Year": 1}).get("Year"),
        "Name":paper_data_collection.find_one({"PaperID": paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
        "Citeref":[]
    }

    for i in cited:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in cited2:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})
    for i in cited3:
        data["Citeref"].append({"Main_Paper":i["Main"],"PaperID":i["PaperID"],"Year":i["Year"],"Name":i["Name"]})

    return jsonify(data)


@app.route('/paper_details/<string:paper_id>', methods=['GET'])
def get_paper_details(paper_id):
    try:
        paper = papers_collection.find_one({"PaperID": paper_id})

        if paper:
            paper_data = paper_data_collection.find_one({"PaperID": paper_id})

            if paper_data:
                references_count = references_collection.count_documents({"Citing_PaperID": paper_id})

                citation_count = paper["Citation_Count"]

                response = {
                    "DOI": paper_data["DOI"],
                    "DocType": paper["DocType"],
                    "Year": paper["Year"],
                    "Reference_Count": references_count,
                    "Citation_Count": citation_count
                }

                return jsonify(response), 200
            else:
                return jsonify({"message": "Paper data not found"}), 404
        else:
            return jsonify({"message": "Paper not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/paper/yearwise', methods=['GET'])
def yearwise():
    paper_id = request.headers.get('Paperid')
    year = request.headers.get('Year')
    year = int(year)
    data = get_paper_citation(paper_id).json
    filtered_citeref = [citation for citation in data["Citeref"] if citation["Year"] == year]
    result = {
        "Paper": data["Paper"],
        "Year": data["Year"],
        "Name": data["Name"],
        "Citeref": filtered_citeref
    }
    return jsonify(result)

def expand_citations(cited):
    expanded_cited = []
    seen_paper_ids = set()

    def add_citations(citations, level):
        next_level_citations = []
        for citation in citations:
            if citation["PaperID"] not in seen_paper_ids:
                papers_cited = references_collection.find({"Cited_PaperID": citation["PaperID"]}, {"Citing_PaperID": 1, "_id": 0})
                for cited_paper in papers_cited:
                    citing_paper_id = cited_paper["Citing_PaperID"]
                    citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1, "Citation_Count": 1, "C10": 1, "Disruption": 1, "Atyp_Median_Z": 1, "Atyp_10pct_Z": 1, "WSB_Cinf": 1})
                    if citing_paper_info:
                        expanded_cited.append({
                            "Main": citation["Main"],
                            "PaperID": citing_paper_id,
                            "Year": citing_paper_info.get("Year"),
                            "Name": paper_data_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
                            "Citation_Count": citing_paper_info.get("Citation_Count"),
                            "C10": citing_paper_info.get("C10"),
                            "Disruption": citing_paper_info.get("Disruption"),
                            "Atyp_Median_Z": citing_paper_info.get("Atyp_Median_Z"),
                            "Atyp_10pct_Z": citing_paper_info.get("Atyp_10pct_Z"),
                            "WSB_Cinf": citing_paper_info.get("WSB_Cinf")
                        })
                        next_level_citations.append({
                            "Main": citation["PaperID"],
                            "PaperID": citing_paper_id,
                            "Year": citing_paper_info.get("Year"),
                            "Name": citing_paper_info.get("Name")
                        })
                seen_paper_ids.add(citation["PaperID"])
        if next_level_citations and level < 3:
            add_citations(next_level_citations, level + 1)

    add_citations(cited, 1)
    return expanded_cited

def expand_references(referenced_by):
    expanded_referenced_by = []
    seen_paper_ids = set()

    def add_references(references, level):
        next_level_references = []
        for reference in references:
            if reference["Main"] not in seen_paper_ids:
                papers_referenced = references_collection.find({"Citing_PaperID": reference["Main"]}, {"Cited_PaperID": 1, "_id": 0})
                for referenced_paper in papers_referenced:
                    referenced_paper_id = referenced_paper["Cited_PaperID"]
                    referenced_paper_info = papers_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1, "Citation_Count": 1, "C10": 1, "Disruption": 1, "Atyp_Median_Z": 1, "Atyp_10pct_Z": 1, "WSB_Cinf": 1})
                    if referenced_paper_info:
                        expanded_referenced_by.append({
                            "Main": referenced_paper_id,
                            "PaperID": reference["Main"],
                            "Year": referenced_paper_info.get("Year"),
                            "Name": paper_data_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
                            "Citation_Count": referenced_paper_info.get("Citation_Count"),
                            "C10": referenced_paper_info.get("C10"),
                            "Disruption": referenced_paper_info.get("Disruption"),
                            "Atyp_Median_Z": referenced_paper_info.get("Atyp_Median_Z"),
                            "Atyp_10pct_Z": referenced_paper_info.get("Atyp_10pct_Z"),
                            "WSB_Cinf": referenced_paper_info.get("WSB_Cinf")
                        })
                        next_level_references.append({
                            "Main": referenced_paper_id,
                            "PaperID": reference["Main"],
                            "Year": referenced_paper_info.get("Year"),
                            "Name": referenced_paper_info.get("Name")
                        })
                seen_paper_ids.add(reference["Main"])
        if next_level_references and level < 3:
            add_references(next_level_references, level + 1)

    add_references(referenced_by, 1)
    return expanded_referenced_by

@app.route('/paper/scientometrics/<string:paper_id>', methods=['GET'])
def scientometrics(paper_id):
    cited = []
    referenced_by = []

    papers_cited = references_collection.find({"Cited_PaperID": paper_id}, {"Citing_PaperID": 1, "_id": 0})
    for cited_paper in papers_cited:
        citing_paper_id = cited_paper["Citing_PaperID"]
        citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1})
        if citing_paper_info:
            cited.append({
                "Main": paper_id,
                "PaperID": citing_paper_id,
                "Year": citing_paper_info.get("Year"),
                "Name": paper_data_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })

    papers_referenced = references_collection.find({"Citing_PaperID": paper_id}, {"Cited_PaperID": 1, "_id": 0})
    for referenced_paper in papers_referenced:
        referenced_paper_id = referenced_paper["Cited_PaperID"]
        referenced_paper_info = papers_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1})
        if referenced_paper_info:
            referenced_by.append({
                "Main": referenced_paper_id,
                "PaperID": paper_id,
                "Year": referenced_paper_info.get("Year"),
                "Name": paper_data_collection.find_one({"PaperID": referenced_paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle")
            })

    expanded_cited = expand_citations(cited)
    expanded_referenced_by = expand_references(referenced_by)

    data = {
        "Paper": paper_id,
        "Year": papers_collection.find_one({"PaperID": paper_id}, {"_id": 0, "Year": 1}).get("Year"),
        "Name": paper_data_collection.find_one({"PaperID": paper_id}, {"_id": 0, "PaperTitle": 1}).get("PaperTitle"),
        "Citeref": expanded_cited + expanded_referenced_by
    }

    return jsonify(data)

@app.route('/paper/filtered', methods=['GET'])
def filtered():
    paper_id = request.headers.get('Paperid')
    min_citation_count = request.headers.get('Min_Citation_Count')
    c10 = request.headers.get('C10')
    disruption = request.headers.get('Disruption')
    atyp_median_z = request.headers.get('Atyp_Median_Z')
    atyp_10pct_z = request.headers.get('Atyp_10pct_Z')
    wsb_cinf = request.headers.get('WSB_Cinf')
    
    filters = {}
    if min_citation_count and min_citation_count.isdigit():
        filters["Citation_Count"] = {"$gte": int(min_citation_count)}
    if c10 and c10.isdigit():
        filters["C10"] = {"$gte": int(c10)}
    if disruption and disruption.replace('.', '', 1).isdigit():
        filters["Disruption"] = {"$gte": float(disruption)}
    if atyp_median_z and atyp_median_z.replace('.', '', 1).isdigit():
        filters["Atyp_Median_Z"] = {"$gte": float(atyp_median_z)}
    if atyp_10pct_z and atyp_10pct_z.replace('.', '', 1).isdigit():
        filters["Atyp_10pct_Z"] = {"$gte": float(atyp_10pct_z)}
    if wsb_cinf and wsb_cinf.replace('.', '', 1).isdigit():
        filters["WSB_Cinf"] = {"$gte": float(wsb_cinf)}


    data = scientometrics(paper_id).json

    def filter_citations(citation):
        for key, value in filters.items():
            if key == "Citation_Count":
                if citation["Scientometrics"].get(key) is None or citation["Scientometrics"][key] < value["$gte"]:
                    return False
            elif citation["Scientometrics"].get(key) != value:
                return False
        return True

    filtered_citeref = [citation for citation in data["Citeref"] if filter_citations(citation)]

    result = {
        "Paper": data["Paper"],
        "Year": data["Year"],
        "Name": data["Name"],
        "Citeref": filtered_citeref
    }

    return jsonify(result)


def get_cited_papers(paper_id):
    return list(references_collection.find({"Cited_PaperID": paper_id}, {"Citing_PaperID": 1, "_id": 0}))

def get_referenced_papers(paper_id):
    return list(references_collection.find({"Citing_PaperID": paper_id}, {"Cited_PaperID": 1, "_id": 0}))


@app.route('/paper/patent_citations/<string:paper_id>', methods=['GET'])
def get_patent_citations(paper_id):
    try:
        
        patent_data = papers_collection.find({"PaperID": paper_id}, {"_id": 0, "PaperID": 1, "Patent_Count": 1})

        patent_data_list = list(patent_data)
        return jsonify(patent_data_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/paper/clinical_trial_citations/<string:paper_id>', methods=['GET'])
def get_clinical_trial_citations(paper_id):
    try:
        clinical_data = papers_collection.find({"PaperID":  paper_id}, {"_id": 0, "PaperID": 1, "NCT_Count": 1})
        clinical_data_list=list(clinical_data)
        return jsonify(clinical_data_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/paper/social_media_influence/<string:paper_id>', methods=['GET'])
def get_social_media_influence(paper_id):
    try:
        
        social_media_data = papers_collection.find({"PaperID":  paper_id}, {"_id": 0, "PaperID": 1, "Newsfeed_Count": 1, "Tweet_Count": 1})
        social_media_data_list=list(social_media_data)
        return jsonify(social_media_data_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/paper/funding_data/<string:paper_id>', methods=['GET'])
def get_funding_data(paper_id):
    try:
        funding_data = papers_collection.find({"PaperID": paper_id}, {"_id": 0, "PaperID": 1, "NIH_Count": 1, "NSF_Count": 1})
        finding_data_list=list(funding_data)
        return jsonify(finding_data_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# @app.route('/paper/nobel_prize/<string:paper_id>', methods=['GET'])
# def get_nobel_prize_data(paper_id):
#     try:
        
#         nobel_data = list(papers_collection.find({"PaperID": paper_id}, {"_id": 0, "PaperID": 1, "Link_NobelLaureates": 1}))
#         nobel_data = [{"PaperID": p["PaperID"], "Nobel_Prize_Winner": "Link_NobelLaureates" in p} for p in nobel_data]
        
#         return jsonify(nobel_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500


@app.route('/author/impact/<string:author_id>', methods=['GET'])
def get_author_impact(author_id):
    try:
        author_id = int(author_id)
        author_data = author_collection.find_one({"AuthorID": author_id})

        if author_data:
            response = {
                "Name": author_data["Author_Name"],
                "h-index": author_data.get("H-index"),
                "Authors Productivity": author_data.get("Productivity"),
                # "Average C10": author_data.get("average_c10")
            }

            return jsonify(response), 200
        else:
            return jsonify({"message": "Author not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/affiliation/impact/<string:affiliation_id>', methods=['GET'])
def get_affiliation_impact(affiliation_id):
    try:
        affiliation_id=int(affiliation_id)
        affiliation_data = affiliation_collection.find_one({"AffiliationID": affiliation_id})

        if affiliation_data:
            response = {
                "Name": affiliation_data["Affiliation_Name"],
                "h-index": affiliation_data.get("H-index"),
                "Affiliation Productivity": affiliation_data.get("Productivity"),
                "Average C10": affiliation_data.get("Average_C10")
            }

            return jsonify(response), 200
        else:
            return jsonify({"message": "Affiliation not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/paper/metrics/<string:paper_id>', methods=['GET'])
def get_paper_metrics(paper_id):
    try:
        paper_id=int(paper_id)
        paper = papers_collection.find_one({"PaperID": paper_id})

        if paper:
            response = {
                
            }

            return jsonify(response), 200
        else:
            return jsonify({"message": "Paper not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


















if __name__ == '__main__':
    app.run(debug=True)














# @app.route('/paper/patent_citations/<string:paper_id>', methods=['GET'])
# def get_cited_patent_citations(paper_id):
#     try:
#         cited_papers = get_cited_papers(paper_id)
#         cited_paper_ids = [p['Citing_PaperID'] for p in cited_papers]
#         cited_patent_data = list(papers_collection.find({"PaperID": {"$in": cited_paper_ids}}, {"_id": 0, "PaperID": 1, "Patent_Count": 1}))
#         return jsonify(cited_patent_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/referenced_patent_citations/<string:paper_id>', methods=['GET'])
# def get_referenced_patent_citations(paper_id):
#     try:
#         referenced_papers = get_referenced_papers(paper_id)
#         referenced_paper_ids = [p['Cited_PaperID'] for p in referenced_papers]
#         referenced_patent_data = list(papers_collection.find({"PaperID": {"$in": referenced_paper_ids}}, {"_id": 0, "PaperID": 1, "Patent_Count": 1}))
#         return jsonify(referenced_patent_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/cited_clinical_trial_citations/<string:paper_id>', methods=['GET'])
# def get_cited_clinical_trial_citations(paper_id):
#     try:
#         cited_papers = get_cited_papers(paper_id)
#         cited_paper_ids = [p['Citing_PaperID'] for p in cited_papers]
#         cited_clinical_data = list(papers_collection.find({"PaperID": {"$in": cited_paper_ids}}, {"_id": 0, "PaperID": 1, "NCT_Count": 1}))
#         return jsonify(cited_clinical_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/referenced_clinical_trial_citations/<string:paper_id>', methods=['GET'])
# def get_referenced_clinical_trial_citations(paper_id):
#     try:
#         referenced_papers = get_referenced_papers(paper_id)
#         referenced_paper_ids = [p['Cited_PaperID'] for p in referenced_papers]
#         referenced_clinical_data = list(papers_collection.find({"PaperID": {"$in": referenced_paper_ids}}, {"_id": 0, "PaperID": 1, "NCT_Count": 1}))
#         return jsonify(referenced_clinical_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/cited_social_media_influence/<string:paper_id>', methods=['GET'])
# def get_cited_social_media_influence(paper_id):
#     try:
#         cited_papers = get_cited_papers(paper_id)
#         cited_paper_ids = [p['Citing_PaperID'] for p in cited_papers]
#         cited_social_media_data = list(papers_collection.find({"PaperID": {"$in": cited_paper_ids}}, {"_id": 0, "PaperID": 1, "Newsfeed_Count": 1, "Tweet_Count": 1}))
#         return jsonify(cited_social_media_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/referenced_social_media_influence/<string:paper_id>', methods=['GET'])
# def get_referenced_social_media_influence(paper_id):
#     try:
#         referenced_papers = get_referenced_papers(paper_id)
#         referenced_paper_ids = [p['Cited_PaperID'] for p in referenced_papers]
#         referenced_social_media_data = list(papers_collection.find({"PaperID": {"$in": referenced_paper_ids}}, {"_id": 0, "PaperID": 1, "Newsfeed_Count": 1, "Tweet_Count": 1}))
#         return jsonify(referenced_social_media_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/cited_funding_data/<string:paper_id>', methods=['GET'])
# def get_cited_funding_data(paper_id):
#     try:
#         cited_papers = get_cited_papers(paper_id)
#         cited_paper_ids = [p['Citing_PaperID'] for p in cited_papers]
#         cited_funding_data = list(papers_collection.find({"PaperID": {"$in": cited_paper_ids}}, {"_id": 0, "PaperID": 1, "NIH_Count": 1, "NSF_Count": 1}))
#         return jsonify(cited_funding_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/referenced_funding_data/<string:paper_id>', methods=['GET'])
# def get_referenced_funding_data(paper_id):
#     try:
#         referenced_papers = get_referenced_papers(paper_id)
#         referenced_paper_ids = [p['Cited_PaperID'] for p in referenced_papers]
#         referenced_funding_data = list(papers_collection.find({"PaperID": {"$in": referenced_paper_ids}}, {"_id": 0, "PaperID": 1, "NIH_Count": 1, "NSF_Count": 1}))
#         return jsonify(referenced_funding_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/cited_nobel_prize/<string:paper_id>', methods=['GET'])
# def get_cited_nobel_prize(paper_id):
#     try:
#         cited_papers = get_cited_papers(paper_id)
#         cited_paper_ids = [p['Citing_PaperID'] for p in cited_papers]
#         cited_nobel_data = list(papers_collection.find({"PaperID": {"$in": cited_paper_ids}}, {"_id": 0, "PaperID": 1, "Link_NobelLaureates": 1}))
#         cited_nobel_data = [{"PaperID": p["PaperID"], "Nobel_Prize_Winner": "Link_NobelLaureates" in p} for p in cited_nobel_data]
#         return jsonify(cited_nobel_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# @app.route('/paper/referenced_nobel_prize/<string:paper_id>', methods=['GET'])
# def get_referenced_nobel_prize(paper_id):
#     try:
#         referenced_papers = get_referenced_papers(paper_id)
#         referenced_paper_ids = [p['Cited_PaperID'] for p in referenced_papers]
#         referenced_nobel_data = list(papers_collection.find({"PaperID": {"$in": referenced_paper_ids}}, {"_id": 0, "PaperID": 1, "Link_NobelLaureates": 1}))
#         referenced_nobel_data = [{"PaperID": p["PaperID"], "Nobel_Prize_Winner": "Link_NobelLaureates" in p} for p in referenced_nobel_data]
#         return jsonify(referenced_nobel_data), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500























# const data={
#         "Paper":"5678",
#         "Citeref": [
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "5678901",
#                 "Year": 2020
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "7890123",
#                 "Year": 2018
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "8901234",
#                 "Year": 2017
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "234567",
#                 "Year": 2013
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "45678",
#                 "Year": 2011
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "78",
#                 "Year": 2008
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "9",
#                 "Year": 2006
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "2345678",
#                 "Year": 2023
#             },
#             {
#                 "Main_Paper": "5678",
#                 "PaperID": "4567890",
#                 "Year": 2021
#             },
#             {
#                 "Main_Paper": "678",
#                 "PaperID": "5678",
#                 "Year": 2009
#             }
#         ]
#     }

# for cite in cited:
    #     papers_cited = references_collection.find({"Cited_PaperID": cite["PaperID"]}, {"Citing_PaperID": 1, "_id": 0})
    #     for cited_paper in papers_cited:
    #         citing_paper_id = cited_paper["Citing_PaperID"]
    #         citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"_id": 0, "Year": 1})
    #         if citing_paper_info:
    #             cited2.append({
    #                 "PaperID": citing_paper_id,
    #                 "Year": citing_paper_info.get("Year")
    #             })

# for refer in referenced_by:
#         papers_referenced = references_collection.find({"Citing_PaperID": refer["PaperID"]}, {"Cited_PaperID": 1, "_id": 0})
#         for referenced_paper in papers_referenced:
#             referenced_paper_id = referenced_paper["Cited_PaperID"]
#             referenced_paper_info = db["paper"].find_one({"PaperID": referenced_paper_id}, {"_id": 0, "Year": 1})
#             if referenced_paper_info:
#                 referenced_by2.append({
#                     "PaperID": referenced_paper_id,
#                     "Year": referenced_paper_info.get("Year")
#                 })
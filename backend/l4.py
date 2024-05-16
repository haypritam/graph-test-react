from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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

if __name__ == '__main__':
    app.run(debug=True)





































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
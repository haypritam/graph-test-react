from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["dummy"]



@app.route('/papers', methods=['GET'])
def get_papers():
    papers_collection = db["paperData"]  # Update collection name to "paperData"
    papers = list(papers_collection.find({}, {"_id": 0}))
    return jsonify(papers)


@app.route('/references', methods=['GET'])
def get_references():
    references_collection = db["reference"]
    references = list(references_collection.find({}, {"_id": 0}))
    return jsonify(references)


@app.route('/paper/<string:paper_id>', methods=['GET'])
def get_paper_by_id(paper_id):
    papers_collection = db["paperData"]  # Update collection name to "paperData"
    paper = papers_collection.find_one({"PaperID": paper_id}, {"_id": 0})
    if paper:
        return jsonify(paper)
    else:
        return jsonify({"error": "PaperID not found"}), 404


@app.route('/paper/details', methods=['GET'])
def get_paper_details_by_title():
    paper_title_input = request.headers.get('PaperTitle')

    if not paper_title_input:
        return jsonify({'error': 'PaperTitle header is required'}), 400

    papers_collection = db["paperData"]  # Update collection name to "paperData"
    references_collection = db["reference"]
    authors_collection = db["auth"]
    auth_aff_collection = db["authaff"]

    paper = papers_collection.find_one({"PaperTitle": paper_title_input})
    if paper is None:
        return jsonify({"error": f"Paper with title '{paper_title_input}' not found"}), 404

    paper_id = paper["PaperID"]
    num_citations = references_collection.count_documents({"Cited_PaperID": paper_id})
    num_references = references_collection.count_documents({"Citing_PaperID": paper_id})

    authors_info = []
    authors = auth_aff_collection.find({"PaperID": paper_id})
    for author in authors:
        author_info = authors_collection.find_one({"AuthorID": author["AuthorID"]})
        if author_info:
            authors_info.append({"AuthorID": author["AuthorID"], "AuthorName": author_info["Author_Name"],
                                 "AffiliationID": author["AffiliationID"]})

    for author_info in authors_info:
        affiliation_info = db["aff"].find_one({"AffiliationID": author_info["AffiliationID"]})
        if affiliation_info:
            author_info["AffiliationName"] = affiliation_info["Affiliation_Name"]

    papers_cited_this_paper = []
    papers_cited = references_collection.find({"Cited_PaperID": paper_id}, {"Citing_PaperID": 1, "_id": 0})
    for cited_paper in papers_cited:
        citing_paper_id = cited_paper["Citing_PaperID"]
        citing_paper_info = papers_collection.find_one({"PaperID": citing_paper_id}, {"Year": 1, "_id": 0})
        if citing_paper_info:
            papers_cited_this_paper.append({"PaperID": citing_paper_id, "Year": citing_paper_info["Year"]})

    papers_referenced_by_this_paper = []
    papers_referenced = references_collection.find({"Citing_PaperID": paper_id}, {"Cited_PaperID": 1, "_id": 0})
    for referenced_paper in papers_referenced:
        referenced_paper_id = referenced_paper["Cited_PaperID"]
        referenced_paper_info = papers_collection.find_one({"PaperID": referenced_paper_id}, {"Year": 1, "_id": 0})
        if referenced_paper_info:
            papers_referenced_by_this_paper.append({"PaperID": referenced_paper_id, "Year": referenced_paper_info["Year"]})

    release_year = paper["Year"]
    current_year = datetime.now().year

    citations_within_5_years = 0
    citations_after_5_years = 0
    for reference in references_collection.find({"Cited_PaperID": paper_id}):
        citing_paper_year = papers_collection.find_one({"PaperID": reference["Citing_PaperID"]}, {"Year": 1, "_id": 0})["Year"]
        if citing_paper_year - release_year <= 5:
            citations_within_5_years += 1
        else:
            citations_after_5_years += 1

    if citations_within_5_years > citations_after_5_years:
        citation_status = "early riser"
    elif citations_within_5_years < citations_after_5_years:
        citation_status = "delay riser"
    else:
        citation_status = "equal"

    return jsonify({
        "PaperID": paper_id,
        "NumCitations": num_citations,
        "NumReferences": num_references,
        "Authors": authors_info,
        "PapersCitedThisPaper": papers_cited_this_paper,
        "PapersReferencedByThisPaper": papers_referenced_by_this_paper,
        "CitationStatus": citation_status
    })


if __name__ == '__main__':
    app.run(debug=True)

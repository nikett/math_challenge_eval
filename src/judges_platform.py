# Input= the submitted entries data tsv
# 1. Generate 38 (or xxx) number of html pages. Each web page has entry id and a secret passcode field for the judges and art work link and judging criteria and points
# 2. On submission on any form, a web service on the form will be invoked.
# 3. This will add an entry to the excel sheet.
import csv
import os
from typing import Dict, Any, List

from src.utils import ensure_path, save_to_file, split_csv


# (future_todo) a cleaner way would be to use a class with the following entries.
# entry metadata (entry_id, entry_category, entry_statement, entry_urls, entry_student_first_name,
#                 entry_student_last_name, entry_student_teacher_name, entry_grade, entry_parent_email_id, entry_file_types)
# judge_name
# judge_secret
# interpretation
# interpretation_comments
# creativity
# creativity_comments
# technique
# technique_comments
# confidence
# other_comments


# <body onload="parse_remote_csv()">
def fill_overall_template(form_arr, entry_ids, judges):
    head = ''' 
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
  background-color: pink;
}
.button {
        display: inline-block;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        color: #ffffff;
        background-color: #2196F3;
        border-radius: 6px;
        outline: none;
}
</style>
</head>
<body>
<div>
<h3> Welcome judges. Please evaluate your entries. <br><br>
</div>
<div id="refresh_status" style="background-color:yellow; width:140px;">
    Updating entries...
</div><br>
'''
    # body = '<p id="http://www.shrikrishnajewels.com/compile/kirtans/1/1.mp3">Kirtan 1: and its <a href="forms/form1.html">link is this</a> </p>'
    rows = []  # for every row, there is an array.
    newline= "\n"
    max_in_one_col = 3
    max_kirtans_in_one_col = 20
    curr_tr_closed = False

    # TODO check if we can access an html page in a google drive.

    # table at main/index.html
    # entry id -- judge1, judge2, judge3, judge4, judge5
    #    1         done    done     xxx     xxx    done
    #  ...
    # TODO read is_evaluated status from a google sheet.

    # can make this less hardcoded.
    headers = ["Entry","..."]
    for judge in judges:
        headers.append(f"Judge {str.capitalize(judge)}")

    rows.append(f"<tr>{newline.join(['<th>' + x + '</th>' + newline for x in headers])}</tr>\n")
    for form_full_path, entry_id in zip(form_arr, entry_ids):
        rows.append(f'<tr>')
        rows.append(f'\n\t<td id=f"entry_{entry_id}"> <a href="{form_full_path}">Entry {entry_id}</a></td>')
        rows.append(f'\n\t<td id=f"dummy_{entry_id}">  </td>')
        for judge in judges:
            rows.append(f'\n\t<td id=f"judge_{judge.lower()}_{entry_id}"> x </td>')
        rows.append('</tr>')

    body = '\n<table style=\"border:2px solid blue;border-collapse:collapse; \">' + '\n'.join(rows) + '\n</table>'
    tail='''
</body>
</html>
'''
    return f"{head}\n\n{body}\n\n{tail}"


def img_and_other_elems(file_types, urls):
    arr = []
    # <img src=url width="500" height="600">
    # <a href="url" target="_blank"> original link</a>
    for file_type, url in zip(file_types, urls):
        if file_type == "jpg":
            # perhaps: create thumbnail from url
            # https://drive.google.com/file/d/14hz3ySPn-zB
            # https://drive.google.com/thumbnail?id=14hz3ySPn-zB
            arr.append(f'<img src="{url}" width="500" height="600">')
            arr.append(f'<a href="{url}" target="_blank">Original image link</a>')
        # TODO handle other file types mp3, mp4, pdf etc.
        # elif file_type == "mp3":
        #     arr.append(f'<audio src={url} width="500" height="600">')
        #     arr.append(f'<a href={url}>Original image link</a>')
        else:
            arr.append(f'<a href="{url}" target="_blank">Original link (file type: {file_type})</a>')

    return "\n<br><br>".join(arr)

def fill_form_template(form_action: str, data: Dict[str, Any]):
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <title>Judging</title>
    <style>
    .button {
        display: inline-block;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        color: #ffffff;
        background-color: #2196F3;
        border-radius: 6px;
        outline: none;
}
</style>
</head>
''' + f'''


<body>
<p><br/>
</p>
<div class="w3-container">
    <div class="w3-container w3-blue">
        <h5>Entry # {data['entry_id']}  &rarr;  ({data['entry_category']})</h5>
    </div><br>
</div>
<form action="{form_action}" class="w3-container" method="GET">
    <input id="entry_student_first_name" name="entry_student_first_name" value="{data['entry_student_first_name']}" type="hidden" readonly/><br/>
    <input id="entry_student_last_name" name="entry_student_last_name" value="{data['entry_student_last_name']}" type="hidden" readonly/><br/>
    <input id="entry_student_teacher_name" name="entry_student_teacher_name" value="{data['entry_student_teacher_name']}" type="hidden" readonly/><br/>
    <input id="entry_grade" name="entry_grade" value="{data['entry_grade']}" type="hidden" readonly/><br/>
    <input id="entry_parent_email_id" name="entry_parent_email_id" value="{data['entry_parent_email_id']}" type="hidden" readonly/><br/>
    <input id="entry_file_types" name="entry_file_types" value="{data['entry_file_types']}"  type="hidden" readonly/>
    <input id="entry_statement" name="entry_statement" value="{data['entry_statement']}"  type="hidden" readonly/>
    <input id="entry_urls" name="entry_urls" value="{data['entry_urls']}"  type="hidden" readonly/>
    <input id="entry_id" name="entry_id" value="{data['entry_id']}" type="hidden" readonly/>
    <input id="entry_category" name="entry_category" value="{data['entry_category']}" type="hidden" readonly/>
    <input id="judge_secret" name="judge_secret" value="dummy" type="hidden" readonly/>
    
    <div class="w3-card-4">
        {img_and_other_elems(file_types=split_csv(data['entry_file_types']), urls=split_csv(data['entry_urls']))}
        
        <p> Caption: {data['entry_statement']}
        </p>
        
        <table>
            <tr>
                <td><label for="judge_name">Your name</label></td>
                <td><input placeholder="" id="judge_name" name="judge_name" type="text" required/></td>
            </tr>
            
            <tr>
                <td><label for="interpretation">Interpretation</label></td>
                <td><input placeholder="" id="interpretation" name="interpretation" type="text" required/></td>
            </tr>
            <tr>
                <td><label for="interpretation_comments">Interpretation comments</label></td>
                <td><input placeholder="" id="interpretation_comments" name="interpretation_comments" type="text"/></td>
            </tr>
            
            <tr>
                <td><label for="creativity">creativity</label></td>
                <td><input placeholder="" id="creativity" name="creativity" type="text" required/></td>
            </tr>
            <tr>
                <td><label for="creativity_comments">creativity comments</label></td>
                <td><input placeholder="" id="creativity_comments" name="creativity_comments" type="text"/></td>
            </tr>
            
            <tr>
                <td><label for="technique">technique</label></td>
                <td><input placeholder="" id="technique" name="technique" type="text"/></td>
            </tr>
            <tr>
                <td><label for="technique_comments">technique comments</label></td>
                <td><input placeholder="" id="technique_comments" name="technique_comments" type="text"/></td>
            </tr>
            
            <tr>
                <td><label for="confidence">Confidence</label></td>
                <td><select id="confidence" name="confidence">
                    <option value="Not confident">Not confident</option>
                    <option value="Sort of confident">Sort of confident</option>
                    <option value="Very confident">Very confident</option>
                </select></td>
            </tr>

            <tr>
                <td><hr /></td>
                <td><hr /></td>
            </tr>

            <tr>
                <td><label for="other_comments"> Other comments </label></td>
                <td><input placeholder="" id="other_comments" name="other_comments" type="text"/></td>
            </tr>
        </table>
    </div>
    
    </div><br>
    <div style="text-align: center;">
        <input class="button" type="submit" value="Submit""/>
    </div>
</form>
</body>
</html>
'''


def rename_dict_keys(d):
    # GIVEN:
    # Timestamp,Email Address,Student first name,Student last name,Grade,Teacher's  name,
    # Upload entry form with file name as (firstname.lastname.grade.pdf) ,
    # Select the art category for submission,Upload entry file,
    # Are the file names you are uploading like so  (firstname.lastname.grade.pdf) ?,
    # Does your artwork follow the submission guidelines (size/format etc.)?,
    # Artist's statement,Are you submitting again with updates?,id,is_valid_final_entry,file_type,
    # Artwork details

    # EXPECTED:
    # entry_id, entry_category, entry_statement, entry_urls, entry_student_first_name,
    # entry_student_last_name, entry_student_teacher_name, entry_parent_email_id, entry_file_types
    d["entry_id"] = d["id"]
    d["entry_category"] = d["Select the art category for submission"]
    d["entry_statement"] = d["Artist's statement"]
    d["entry_urls"] = d["Upload entry file"]
    d["entry_student_first_name"] = d["Student first name"]
    d["entry_student_last_name"] = d["Student last name"]
    d["entry_student_teacher_name"] = d["Teacher's  name"]
    d["entry_grade"] = d["Grade"]
    d["entry_parent_email_id"] = d["Email Address"]
    d["entry_file_types"] = d["file_type"]
    return d


def load_data_to_forms(fp, out_dir, form_action, website_base_addr, judges):

    index_html = f"{out_dir}/index.html"
    successful_forms = 0
    with open(fp) as f_handle:
        form_online_paths_arr = []
        entry_id_arr = []
        for d in csv.DictReader(f_handle):
            id_ = d["id"]
            fname = f'{id_}.html'
            rename_dict_keys(d)
            form_path_local = os.path.join(out_dir, fname)
            html_form_content = fill_form_template(form_action=form_action, data=d)
            save_to_file(content=html_form_content, out_fp=form_path_local)
            form_path_online = os.path.join(website_base_addr, fname)
            print(f"{form_path_online}'s form : {form_path_local}")
            form_online_paths_arr.append(form_path_online)
            entry_id_arr.append(id_)
            successful_forms += 1
        print(f"Saving index.html to {index_html}")
        save_to_file(content=fill_overall_template(form_arr=form_online_paths_arr, entry_ids=entry_id_arr, judges=judges),
                     out_fp=index_html)
        return successful_forms


def main(data_entries_fp: str, out_dir: str, judges: List[str], website_base_addr: str, form_action: str):
    """
    :param data_entries_fp: "data/judges_input/real-judges-data.csv"
    :param out_dir: "data/forms"
    :param judges: ["Dhivya", "Shweta", "Thom", "Trisha", "Whitney"]
    :param website_base_addr: "file://" # http://www.shrikrishnajewels.com/compile/forms
    :param form_action: "https://script.google.com/macros/s/AKfycbxM03CgaCSU5PsWahgEa6RLpPZXIm8mhDMEPofdkDJ-1iLjZCv1HiJxr_BU3NlunTYJoQ/exec"
    :return:
    """
    assert os.path.exists(data_entries_fp), f"\n\ndata entries (input csv) for judges does not exist: {data_entries_fp}"
    ensure_path(fp=out_dir, is_dir=True)
    return load_data_to_forms(fp=data_entries_fp,
                       out_dir=out_dir,
                       judges=judges,
                       website_base_addr=website_base_addr,
                       form_action=form_action)

if __name__ == '__main__':
    main(data_entries_fp= "data/judges_input/real-judges-data.csv",
         out_dir= "data/forms",
         judges =["Dhivya", "Shweta", "Thom", "Trisha", "Whitney"],
         website_base_addr = "",
         form_action="https://script.google.com/macros/s/AKfycbxM03CgaCSU5PsWahgEa6RLpPZXIm8mhDMEPofdkDJ-1iLjZCv1HiJxr_BU3NlunTYJoQ/exec"
         )
#!/usr/bin/env python
# encoding: utf-8


import requests, json

from xmind2testlink.datatype import TestCase


class xray_issue:

    def create_xray_issue(project_name_key, issue_name, jira_token, importance):
        url = "https://olapio.atlassian.net/rest/api/2/issue"
        importance_list = [0, 1, 2, 3]
        if importance is not None:
            if int(importance) not in importance_list:
                importance = 3
        else:
            return
        issue_name = str(issue_name).replace('\r\n', '')
        payload = {
            "fields": {"project": {"key": project_name_key},
                       "summary": issue_name,
                       "priority": {"name": "P" + str(importance)},
                       "description": "example of manual test",
                       "customfield_10048":[{"id": "10168"}],
                       "customfield_10137":  {"id": "10204"},
                       "customfield_10146": {"id": "10224"},
                       "customfield_10139": {"id": "10206"},
                       "customfield_10145": {"id": "10216"},
                       "customfield_10089": {"id": "10133"},
                       "assignee":{"accountId": "5d74c661cdb6650c4bf7ffda"},
                       "issuetype": {"name": "Test"}}}
        headers = {
            'Authorization': 'Basic ' + jira_token,
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.json())
        print('成功创建了xray issue https://olapio.atlassian.net/browse/' + response.json()['key'])
        return response.json()['id'], response.json()['key']

    # 2. 给issue新增step, 替换url中的id

    def create_xray_issue_step(key, index, action, data, result, X_acpt):
        headers = {
            'X-acpt': X_acpt,
            'Content-Type': 'application/json;charset=UTF-8',
        }

        data = {"id": "-1", "index": index, "customFields": [], "action": action, "data": data, "result": result}

        response = requests.post('https://xray.cloud.xpand-it.com/api/internal/test/' + key + '/step', headers=headers,
                                 data=json.dumps(data))
        print(response.json())
        print(response.status_code)
        if response.status_code == 401:
            print(response.json()['error'])
            exit(1)
        # else:
        #     print('创建步骤成功')

    def create_xray_full_issue(project_name_key, issue_name, test_case, link_issue_key, jira_token, X_acpt):
        # test_case = TestCase(test_case)
        if test_case.importance is None:
            print('no importance')
            return
        (id, key) = xray_issue.create_xray_issue(project_name_key, issue_name, jira_token, test_case.importance)
        xray_issue.link_issue(link_issue_key, key, jira_token)

        for i in range(len(test_case.steps)):
            step = test_case.steps[i]
            xray_issue.create_xray_issue_step(id, i, step.action, '', step.expected, X_acpt)

    def link_issue(origin_key, xray_key, jira_token):
        url = 'https://olapio.atlassian.net/rest/api/2/issueLink'

        # payload = {"type": {"id": "10006"}, "inwardIssue": {"key": "KE-12706"}, "outwardIssue": {"key": "QUARD-263"}}
        payload = {"type": {"id": "10006"}, "inwardIssue": {"key": origin_key}, "outwardIssue": {"key": xray_key}}
        headers = {
            'Authorization': 'Basic ' + jira_token,
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        # return response.json()['id']

    def get_issue_info(self):
        import requests

        url = "https://olapio.atlassian.net/rest/api/2/issue/QUARD-263"

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + jira_token,
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))


# create_xray_full_issue()
if __name__ == '__main__':
    # X_acpt = ''
    jira_token = 'd2VpLnpob3VAa3lsaWdlbmNlLmlvOm8xeGh0M2owSVdheUdxWWx4bUUwNzU2Rg=='
    xray_issue = xray_issue()
    xray_issue.get_issue_info()
    # project_name_key = 'QUARD'
    # issue_name = 'test_issue'
    # test_case = ''
    # link_issue_key = ''
    # xray_issue.create_xray_full_issue(project_name_key, issue_name, test_case, link_issue_key)

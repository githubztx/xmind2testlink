"""
A tool to parse xmind file into testlink xml file, which will help
you generate a testlink recognized xml file, then you can import it
into testlink as test suites.

Usage:
 xmind2testlink [path_to_xmind_file] [-json]

Example:
 xmind2testlink C:\\tests\\testcase.xmind       => output xml
 xmind2testlink C:\\tests\\testcase.xmind -json => output json

"""

import json
import sys, argparse

from xmind2testlink.testlink_parser import to_testlink_xml_file
from xmind2testlink.xmind_parser import xmind_to_suite, xmind_to_flat_dict
from xmind2testlink.xray import xray_issue


def xmind_to_testlink(xmind):
    xml_out = xmind[:-5] + 'xml'
    suite = xmind_to_suite(xmind)
    to_testlink_xml_file(suite, xml_out)
    return xml_out


def xmind_to_json(xmind):
    json_out = xmind[:-5] + 'json'
    with open(json_out, 'w', encoding='utf8') as f:
        f.write(json.dumps(xmind_to_flat_dict(xmind), indent=2))

    return json_out


def get_issue_key(test_case_name):
    chn_index = str(test_case_name).find('：')

    en_index = str(test_case_name).find(':')

    if chn_index == -1 and en_index == -1:
        issue_key_index = -1
    elif chn_index == -1:
        issue_key_index = en_index
    elif en_index == -1:
        issue_key_index = chn_index
    else:
        issue_key_index = min(chn_index, en_index)

    if issue_key_index == -1:
        link_issue_key = ''
    else:
        link_issue_key = str(test_case_name)[:issue_key_index]
    return link_issue_key


def main(xacpt, jira_token, project_name_key, xmind):
    suite = xmind_to_suite(xmind)
    for test_suit in suite.sub_suites:
        sub_title = test_suit.name
        for test_case in test_suit.testcase_list:
            test_case_name = test_case.name
            title_name = sub_title + ' > ' + test_case_name
            xray_issue.create_xray_full_issue(project_name_key, title_name,
                                              test_case, get_issue_key(test_case_name), jira_token,
                                              xacpt)
        # for test_case in test_suit
    print()


if __name__ == '__main__':
    xacpt ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb20ueHBhbmRpdC5wbHVnaW5zLnhyYXkiLCJpYXQiOjE2MTQ1OTIzNjIsInN1YiI6IjVkNzRjNjYxY2RiNjY1MGM0YmY3ZmZkYSIsImV4cCI6MTYxNDY3ODc2MiwiYXVkIjpbImNkZWY2OTk3LTk1NDItMzA4OS05MzRjLTQ4NWIxYTcxMTc3ZCJdLCJjb250ZXh0Ijp7ImxpY2Vuc2UiOnsiYWN0aXZlIjp0cnVlfSwiamlyYSI6eyJpc3N1ZSI6eyJpc3N1ZXR5cGUiOnsiaWQiOiIxMDA0MyJ9LCJrZXkiOiJNRFgtMjg5NyIsImlkIjoiNjcwNDEifSwicHJvamVjdCI6eyJrZXkiOiJNRFgiLCJpZCI6IjEwMDIzIn19fX0.11BD9PW-d5CPZx4CurvF5IfLQCUEyPJzE9h4BZo0c8A'
    jira_token = "ZG9uZ2RvbmcuemhvdUBreWxpZ2VuY2UuaW86eFlNOUdpYkZJR21GNUs2Mm42MHNEM0E4"
    project_name_key = "MDX"
    xmind = "/Users/dongdong.zhou/Desktop/MDX-xray.xmind"
    main(xacpt, jira_token, project_name_key, xmind)

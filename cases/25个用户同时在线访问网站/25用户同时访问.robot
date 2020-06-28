*** Settings ***

Library  25用户同时访问.py   WITH NAME  M

Suite Setup    M.suite_setup

Suite Teardown    M.suite_teardown

Library  25用户同时访问.c1   WITH NAME  c1



*** Test Cases ***

25个用户同时在线访问
  [Setup]     c1.setup
  [Teardown]  c1.teardown

  c1.teststeps

*** Settings ***

Library  性能测试.py   WITH NAME  M

Library  性能测试.c1   WITH NAME  c1



*** Test Cases ***

1 台终端演示测试
  [Setup]     c1.setup
  [Teardown]  c1.teardown

  c1.teststeps

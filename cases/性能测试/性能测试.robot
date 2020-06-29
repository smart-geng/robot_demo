*** Settings ***

Library  性能测试.py   WITH NAME  M

Library  性能测试.c1   WITH NAME  c1

Library  性能测试.c2   WITH NAME  c2



*** Test Cases ***

1 台终端演示测试
  [Setup]     c1.setup
  [Teardown]  c1.teardown

  c1.teststeps


200 台终端心跳压力1秒一次
  [Setup]     c2.setup
  [Teardown]  c2.teardown

  c2.teststeps

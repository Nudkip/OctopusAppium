reportPath='./testResult'
current_time=$(date "+%Y%m%d_%H_%M")
# add testCase Class to array
testCasePathArray=()
testCasePathArray+=('test_AppAuthNotification')
# testCasePathArray+=('./test/test_appAuthNotification')


arrayLength=${#testCasePathArray[@]}
# install the new .ipa
# install ios-deploy from 
    # npm i -g ios-deploy
# ios-deploy -i d2868681650f7719f409679663b4af95f71278be -b /Users/raymondc/Documents/Appium/Octopus_VCC.ipa
# ideviceinstaller -u d2868681650f7719f409679663b4af95f71278be -i /Users/raymondc/Documents/Appium/Octopus_VCC.ipa
for(( j=0; j<$arrayLength; j++ ))
do
    testCase=${testCasePathArray[$j]}
    echo running $line
    echo "ON999999"
    # stop after two failures --maxfail=2 
    # shortcut for --capture=no. -s
    # increase verbosity. -v
    # --pdb add pytest.set_trace() in breakPoint
    python3 -m pytest -v -s --fullReset=True --maxfail=1 ${testCase} --html=$reportPath/${testCase}_${current_time}.html --self-contained-html
    # python3 -m pytest -v -s --fullReset=True --maxfail=1 ${testCasePathArray[$j]}.py --self-contained-html
    # python3 -m pytest -v -s --fullReset=True --maxfail=1 ./test --html=$reportPath/index.html --self-contained-html

done


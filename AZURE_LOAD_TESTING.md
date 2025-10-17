# Azure Load Testing Configuration

## Load Test Configuration for MC101 Application

### Test Scenarios

#### 1. Health Endpoint Load Test
- **Target URL**: `https://51.12.210.9/health`
- **Test Duration**: 5 minutes
- **Virtual Users**: 50
- **Ramp-up Time**: 1 minute
- **Expected Response**: 200 OK with JSON health status

#### 2. Non-Existing Endpoint Test
- **Target URL**: `https://51.12.210.9/non-existing`
- **Test Duration**: 2 minutes
- **Virtual Users**: 20
- **Ramp-up Time**: 30 seconds
- **Expected Response**: 404 Not Found

### JMeter Test Plan Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.4.1">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="MC101 Load Test">
      <stringProp name="TestPlan.comments">Load testing for MC101 Notes &amp; Voting API</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.arguments" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        <collectionProp name="Arguments.arguments">
          <elementProp name="SERVER_URL" elementType="Argument">
            <stringProp name="Argument.name">SERVER_URL</stringProp>
            <stringProp name="Argument.value">51.12.210.9</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <!-- Health Endpoint Test -->
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Health Endpoint Load Test">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControllerGui" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <intProp name="LoopController.loops">-1</intProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">50</stringProp>
        <stringProp name="ThreadGroup.ramp_time">60</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">300</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Health Check Request">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">${SERVER_URL}</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/health</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout">10000</stringProp>
          <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
        </HTTPSamplerProxy>
      </hashTree>
      
      <!-- Non-Existing Endpoint Test -->
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Non-Existing Endpoint Test">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControllerGui" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <intProp name="LoopController.loops">-1</intProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">20</stringProp>
        <stringProp name="ThreadGroup.ramp_time">30</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">120</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Non-Existing Endpoint Request">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">${SERVER_URL}</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/non-existing</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout">10000</stringProp>
          <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
        </HTTPSamplerProxy>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### Azure Load Testing Service Setup

#### Step 1: Create Azure Load Testing Resource
1. In Azure Portal, search for "Azure Load Testing"
2. Click "Create" to create a new Load Testing resource
3. Configure the resource:
   - **Resource Group**: Same as your VM resource group
   - **Name**: `mc101-load-testing`
   - **Region**: Same as your VM region
   - **Pricing Tier**: Standard

#### Step 2: Configure IAM Access
1. Go to the Load Testing resource
2. Click "Access control (IAM)"
3. Add role assignment:
   - **Role**: Reader
   - **Assign access to**: User
   - **Email**: `Siamak.khatami@kristiania.no`

#### Step 3: Create Load Test
1. In the Load Testing resource, click "Tests"
2. Click "Create" → "Upload a JMeter script"
3. Upload the JMX file (save the XML content above as `mc101-load-test.jmx`)
4. Configure test parameters:
   - **Test name**: MC101 Application Load Test
   - **Description**: Load testing for health and non-existing endpoints
   - **Engine instances**: 1
   - **Test duration**: 5 minutes

### Expected Results

#### Health Endpoint (`/health`)
- **Expected Response Time**: < 200ms
- **Expected Throughput**: > 100 requests/second
- **Expected Success Rate**: 99%+
- **Response Code**: 200 OK

#### Non-Existing Endpoint (`/non-existing`)
- **Expected Response Time**: < 100ms (faster due to early return)
- **Expected Throughput**: > 200 requests/second
- **Expected Success Rate**: 100% (404 is expected)
- **Response Code**: 404 Not Found

### Test Execution Commands

```bash
# Test health endpoint manually
curl -k -w "\n Response Time: %{time_total}s\n" https://51.12.210.9/health

# Test non-existing endpoint manually
curl -k -w "\n Response Time: %{time_total}s\n" https://51.12.210.9/non-existing

# Continuous monitoring during load test
while true; do
  echo "$(date): Health endpoint response time: $(curl -k -w '%{time_total}' -s -o /dev/null https://51.12.210.9/health)s"
  sleep 5
done
```

### Load Testing IAM Configuration

**Required Access for**: `Siamak.khatami@kristiania.no`
- **Resource**: Azure Load Testing Service
- **Role**: Reader
- **Permissions**: View test results, metrics, and configurations

### Test Results Analysis

After running the load test, analyze:
1. **Response Time Trends**: Monitor for any degradation
2. **Throughput Metrics**: Requests per second under load
3. **Error Rates**: Any failed requests or timeouts
4. **Resource Utilization**: VM CPU/Memory usage during testing
5. **Comparison**: Performance difference between valid and invalid endpoints

### Sharing Test Results

1. **Test Link**: Available in Azure Portal after test completion
2. **Screenshots**: Capture response time graphs, throughput charts, and error rates
3. **Report**: Include in the final project report with analysis
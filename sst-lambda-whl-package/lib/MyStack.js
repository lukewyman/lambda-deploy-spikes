import * as sst from "@serverless-stack/resources";

export default class MyStack extends sst.Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    // Create a HTTP API
    const api = new sst.Api(this, "Api", {
      defaultFunctionProps: {
        srcPath: "src",
        bundle: {
          installCommands: [
            'pip3 install -r requirements.txt',
            'pip3 install -i https://test.pypi.org/simple/ sst-lambda-wheel-libs==0.0.1'
          ]
        }
      },
      routes: {
        "GET /poster": "handlers/poster.handler",
        "GET /getter": "handlers/getter.handler"
      }
    }); 

    // Show the endpoint in the output
    this.addOutputs({
      "ApiEndpoint": api.url,
    });
  }
}

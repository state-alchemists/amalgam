(pulumi stack select {{input.myapp_pulumi_stack}} || pulumi stack init {{input.myapp_pulumi_stack}})
pulumi up --skip-preview
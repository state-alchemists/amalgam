(pulumi stack select {{input.fastapp_pulumi_stack}} || pulumi stack init {{input.fastapp_pulumi_stack}})
pulumi destroy --skip-preview
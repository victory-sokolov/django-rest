{{/*
Set gateway-api.enabled based on routing.type
*/}}
{{ - define "apps.gatewayApiEnabled" - }}
{{ - eq .Values.routing.type "gateway" }}
{{ - end }}

{{/*
Set ingress.enabled based on routing.type
*/}}
{{ - define "apps.ingressEnabled" - }}
{{ - eq .Values.routing.type "ingress" }}
{{ - end }}

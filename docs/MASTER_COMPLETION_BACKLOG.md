# APEX / AMOS — MASTER COMPLETION BACKLOG

## Mission
APEX is the global mobility platform; AMOS is its air-mobility operating system. The platform must support drones, cargo drones, ambulance aircraft, police aircraft, helicopters, electric aircraft, UAVs, autonomous ground vehicles and maritime vehicles through shared identity, mission, safety, traffic, digital-twin and integration infrastructure.

## Non-negotiable architecture principles
1. Mission-centric rather than vehicle-centric operations.
2. Country sovereignty and tenant isolation by default.
3. Cross-border operations only through explicit, minimum-data gateways.
4. Safety-critical decisions remain deterministic/rule-governed; AI is advisory unless separately certified.
5. Every machine and human has a verifiable identity.
6. All safety/security actions are auditable and tamper-evident.
7. Event-driven architecture with durable event history.
8. Edge/degraded operation for loss of cloud connectivity.
9. Internationalization is a platform capability, not a UI afterthought.
10. Every domain must have API, tests, observability, security and migration coverage.

## Completion tracks

### CAP-001 Identity & Access
- [x] Authentication foundation
- [x] Email verification foundation
- [x] Password reset foundation
- [x] MFA/TOTP foundation
- [x] Recovery-code foundation
- [x] Session persistence foundation
- [x] Device persistence foundation
- [ ] Device management API
- [ ] Trusted-device verification flow
- [ ] Session rotation/reuse detection
- [ ] Logout / logout-all
- [ ] Account lockout and brute-force controls
- [ ] Login risk engine
- [ ] Security notifications
- [ ] WebAuthn / passkeys
- [ ] OAuth2/OIDC
- [ ] SAML 2.0 enterprise SSO
- [ ] SCIM provisioning
- [ ] API keys
- [ ] Service accounts
- [ ] Machine identities
- [ ] Vehicle identities
- [ ] RBAC
- [ ] ABAC
- [ ] Relationship-based authorization
- [ ] Policy engine
- [ ] country/org/region/resource scopes
- [ ] immutable identity audit
- [ ] identity event publishing
- [ ] full unit/integration/security test suite

### CAP-002 Organization & Sovereignty
- [ ] Global organization model
- [ ] country tenant
- [ ] sovereign tenant boundary
- [ ] organization hierarchy
- [ ] regional operational units
- [ ] data residency policy
- [ ] country encryption keys
- [ ] country administrators
- [ ] cross-border authorization
- [ ] minimum-data cross-border exchange
- [ ] data retention policies
- [ ] legal hold
- [ ] country-level audit

### CAP-003 PKI / Trust Fabric
- [ ] root CA architecture
- [ ] country CA hierarchy
- [ ] vehicle/device certificates
- [ ] operator certificates
- [ ] service certificates
- [ ] certificate issuance
- [ ] rotation
- [ ] revocation
- [ ] OCSP/CRL
- [ ] mTLS
- [ ] HSM integration boundary
- [ ] key lifecycle

### CAP-004 Manufacturer & Vehicle Registry
- [ ] manufacturer onboarding
- [ ] company verification
- [ ] manufacturer organization
- [ ] vehicle type
- [ ] vehicle model
- [ ] serial/registration identity
- [ ] production vehicle registration
- [ ] certificate records
- [ ] firmware/software versions
- [ ] airworthiness/certification records
- [ ] battery certification
- [ ] autonomous capability declaration
- [ ] payload capability
- [ ] vehicle ownership transfer
- [ ] vehicle suspension/revocation

### CAP-005 FleetOS
- [ ] fleet model
- [ ] vehicle lifecycle
- [ ] operator assignment
- [ ] owner assignment
- [ ] vehicle state
- [ ] vehicle health
- [ ] firmware lifecycle
- [ ] maintenance status
- [ ] insurance status
- [ ] registration status
- [ ] geolocation
- [ ] fleet dashboards

### CAP-006 MissionOS
- [ ] mission aggregate
- [ ] mission lifecycle/state machine
- [ ] mission participants
- [ ] vehicle assignment
- [ ] pilot/operator assignment
- [ ] passenger manifest
- [ ] cargo manifest
- [ ] route
- [ ] corridor
- [ ] weather snapshot
- [ ] energy plan
- [ ] airspace clearance
- [ ] risk assessment
- [ ] mission approval
- [ ] mission scheduling
- [ ] mission cancellation
- [ ] mission completion

### CAP-007 Mission Graph
- [ ] graph data model
- [ ] mission-to-vehicle edges
- [ ] mission-to-route edges
- [ ] mission-to-corridor edges
- [ ] mission-to-weather edges
- [ ] mission-to-energy edges
- [ ] mission-to-regulation edges
- [ ] mission-to-risk edges
- [ ] mission-to-emergency edges
- [ ] graph event history
- [ ] graph query API

### CAP-008 3D GIS / Virtual Corridors
- [ ] 3D globe
- [ ] terrain
- [ ] buildings
- [ ] roads
- [ ] altitude layers
- [ ] virtual air roads/corridors
- [ ] vertical corridors
- [ ] horizontal corridors
- [ ] corridor entry/exit points
- [ ] corridor intersections
- [ ] separation rules
- [ ] restricted areas
- [ ] temporary restrictions
- [ ] landing zones
- [ ] emergency landing zones
- [ ] traffic visualization
- [ ] weather layers

### CAP-009 Airspace & TrafficOS
- [ ] country airspace model
- [ ] sectors
- [ ] traffic control centers
- [ ] controllers/operators
- [ ] clearance workflow
- [ ] traffic state
- [ ] conflict detection
- [ ] conflict prediction
- [ ] separation management
- [ ] route deviation detection
- [ ] speed/altitude violations
- [ ] restricted-zone violations
- [ ] traffic enforcement
- [ ] dynamic corridor management

### CAP-010 EmergencyOS
- [ ] emergency event model
- [ ] priority engine
- [ ] ambulance corridor
- [ ] police/security corridor
- [ ] fire corridor
- [ ] disaster corridor
- [ ] rescue mission
- [ ] emergency landing calculation
- [ ] hospital integration
- [ ] emergency resource availability
- [ ] emergency traffic preemption
- [ ] emergency notifications

### CAP-011 Navigation & Safety
- [ ] route planning
- [ ] terrain awareness
- [ ] obstacle awareness
- [ ] geofencing
- [ ] GNSS integration abstraction
- [ ] GNSS anomaly detection
- [ ] spoofing/jamming detection
- [ ] inertial fallback interface
- [ ] collision risk calculation
- [ ] safe alternative route
- [ ] return-to-safe-state policy

### CAP-012 WeatherOS
- [ ] weather provider abstraction
- [ ] live weather ingestion
- [ ] forecast ingestion
- [ ] wind model
- [ ] visibility
- [ ] precipitation
- [ ] storm/lightning
- [ ] turbulence
- [ ] weather risk scoring
- [ ] mission weather constraints

### CAP-013 EnergyOS
- [ ] battery model
- [ ] SOC
- [ ] SOH
- [ ] energy consumption model
- [ ] range prediction
- [ ] reserve policy
- [ ] charging station
- [ ] charging session
- [ ] charging schedule
- [ ] battery swap
- [ ] degradation model
- [ ] emergency energy policy

### CAP-014 VertiportOS
- [ ] vertiport registry
- [ ] pads/gates
- [ ] arrival/departure scheduling
- [ ] charging
- [ ] security
- [ ] passenger processing
- [ ] cargo processing
- [ ] maintenance slots
- [ ] landing authorization
- [ ] capacity management

### CAP-015 Telemetry & Digital Twin
- [ ] telemetry gateway
- [ ] MQTT/stream ingestion boundary
- [ ] telemetry schema
- [ ] position/altitude/speed/heading
- [ ] battery telemetry
- [ ] propulsion telemetry
- [ ] sensor health
- [ ] connectivity state
- [ ] digital twin vehicle
- [ ] digital twin infrastructure
- [ ] digital twin corridor
- [ ] digital twin airspace
- [ ] real-time state projection

### CAP-016 Simulation
- [ ] mission simulation
- [ ] traffic simulation
- [ ] weather simulation
- [ ] battery simulation
- [ ] emergency simulation
- [ ] collision/conflict simulation
- [ ] scenario library
- [ ] replay
- [ ] simulation-vs-real comparison

### CAP-017 AI Platform
- [ ] AI gateway
- [ ] model registry
- [ ] prompt/model policy
- [ ] route optimization
- [ ] traffic prediction
- [ ] weather risk prediction
- [ ] battery prediction
- [ ] predictive maintenance
- [ ] anomaly detection
- [ ] decision support
- [ ] AI Copilot by role
- [ ] AI auditability
- [ ] model evaluation
- [ ] model rollback
- [ ] human approval for safety-critical actions

### CAP-018 MaintenanceOS
- [ ] maintenance records
- [ ] scheduled maintenance
- [ ] inspection
- [ ] work orders
- [ ] parts
- [ ] technician identity
- [ ] maintenance authorization
- [ ] predictive maintenance integration
- [ ] aircraft grounding state
- [ ] return-to-service approval

### CAP-019 Incident / Safety Management
- [ ] incident
- [ ] accident
- [ ] near miss
- [ ] hazard
- [ ] risk
- [ ] mitigation
- [ ] investigation
- [ ] evidence
- [ ] root-cause analysis
- [ ] corrective actions
- [ ] safety case
- [ ] safety evidence

### CAP-020 Flight Recorder / Evidence
- [ ] immutable mission record
- [ ] telemetry archive
- [ ] operator actions
- [ ] command history
- [ ] warnings
- [ ] AI recommendations
- [ ] evidence attachments
- [ ] cryptographic signatures
- [ ] chain of custody
- [ ] tamper detection
- [ ] retention policy

### CAP-021 Regulation & ComplianceOS
- [ ] regulation registry
- [ ] rule versioning
- [ ] country rules
- [ ] vehicle rules
- [ ] operator rules
- [ ] mission rules
- [ ] airspace rules
- [ ] corridor rules
- [ ] automated compliance checks
- [ ] waiver/exemption workflow
- [ ] compliance evidence

### CAP-022 Passenger & Cargo
- [ ] passenger identity
- [ ] booking
- [ ] boarding
- [ ] baggage
- [ ] passenger manifest
- [ ] cargo manifest
- [ ] weight/volume
- [ ] dangerous goods
- [ ] temperature-controlled cargo
- [ ] chain of custody
- [ ] delivery tracking

### CAP-023 Police / Security Operations
- [ ] police mission
- [ ] patrol
- [ ] surveillance mission
- [ ] interception workflow
- [ ] restricted-area enforcement
- [ ] evidence capture
- [ ] security command center
- [ ] emergency authority override with audit

### CAP-024 Multimodal Mobility
- [ ] LMOS ground domain
- [ ] SMOS maritime domain
- [ ] SPMOS surface/public mobility domain
- [ ] multimodal mission graph
- [ ] autonomous truck integration
- [ ] autonomous ground vehicle integration
- [ ] maritime vehicle integration
- [ ] intermodal transfer
- [ ] unified trip/mission status

### CAP-025 IntegrationOS
- [ ] API gateway
- [ ] REST
- [ ] GraphQL
- [ ] gRPC
- [ ] WebSocket
- [ ] MQTT
- [ ] webhooks
- [ ] ERP integrations
- [ ] OEM integrations
- [ ] airport/vertiport integrations
- [ ] weather integrations
- [ ] government integrations
- [ ] police/emergency integrations
- [ ] telecom/satellite integrations
- [ ] integration credentials
- [ ] integration health

### CAP-026 Event Platform
- [ ] event schema registry
- [ ] event bus
- [ ] durable event storage
- [ ] idempotency
- [ ] retries
- [ ] dead-letter queues
- [ ] event versioning
- [ ] outbox pattern
- [ ] audit event correlation

### CAP-027 NotificationOS
- [ ] in-app
- [ ] email
- [ ] SMS
- [ ] push
- [ ] emergency broadcast
- [ ] operator notification policies
- [ ] localization
- [ ] escalation rules

### CAP-028 Billing / Commercial
- [ ] subscription
- [ ] mission fees
- [ ] airspace fees
- [ ] vertiport fees
- [ ] charging fees
- [ ] API usage billing
- [ ] government billing
- [ ] manufacturer billing
- [ ] invoice
- [ ] payment integration
- [ ] tax abstraction

### CAP-029 Marketplace
- [ ] vehicle marketplace
- [ ] service marketplace
- [ ] maintenance services
- [ ] charging services
- [ ] insurance
- [ ] parts
- [ ] software/services
- [ ] pilot/operator services
- [ ] vertiport services

### CAP-030 Developer Platform
- [ ] developer organizations
- [ ] API credentials
- [ ] OAuth apps
- [ ] API scopes
- [ ] SDKs
- [ ] documentation portal
- [ ] sandbox
- [ ] simulation sandbox
- [ ] webhook management
- [ ] API usage analytics

### CAP-031 Government Platform
- [ ] government tenant
- [ ] national authority
- [ ] regional authority
- [ ] traffic control center
- [ ] airspace administration
- [ ] manufacturer oversight
- [ ] vehicle oversight
- [ ] operator licensing
- [ ] incident investigation
- [ ] national statistics

### CAP-032 Cybersecurity
- [ ] zero-trust architecture
- [ ] WAF
- [ ] DDoS boundary
- [ ] secrets management
- [ ] SIEM integration
- [ ] SOC integration
- [ ] threat detection
- [ ] IDS/IPS integration
- [ ] vulnerability management
- [ ] security incident response
- [ ] privileged access management
- [ ] security audit

### CAP-033 Observability
- [ ] structured logging
- [ ] metrics
- [ ] distributed tracing
- [ ] health endpoints
- [ ] alerting
- [ ] SLI/SLO
- [ ] service dependency graph
- [ ] audit correlation IDs
- [ ] operational dashboards

### CAP-034 Data Platform
- [ ] operational PostgreSQL/PostGIS
- [ ] event stream
- [ ] object storage
- [ ] data lake
- [ ] warehouse
- [ ] ETL/ELT
- [ ] data catalog
- [ ] data quality
- [ ] lineage
- [ ] retention

### CAP-035 Analytics
- [ ] traffic analytics
- [ ] fleet analytics
- [ ] mission analytics
- [ ] energy analytics
- [ ] safety analytics
- [ ] revenue analytics
- [ ] country analytics
- [ ] environmental analytics

### CAP-036 Internationalization
- [ ] locale service
- [ ] translation catalogs
- [ ] terminology management
- [ ] aviation terminology
- [ ] date/time formats
- [ ] number formats
- [ ] currencies
- [ ] units
- [ ] RTL
- [ ] multilingual notifications
- [ ] multilingual regulatory content

### CAP-037 Disaster Recovery / Edge
- [ ] backup
- [ ] restore testing
- [ ] regional failover
- [ ] country failover
- [ ] disaster recovery plan
- [ ] RPO/RTO definitions
- [ ] edge gateway
- [ ] telemetry buffering
- [ ] offline traffic-control mode
- [ ] degraded safety mode
- [ ] reconciliation after reconnect

### CAP-038 Quality / Delivery
- [ ] monorepo/service conventions
- [ ] dependency management
- [ ] migrations per service
- [ ] unit tests
- [ ] integration tests
- [ ] contract tests
- [ ] end-to-end tests
- [ ] security tests
- [ ] load tests
- [ ] chaos tests
- [ ] simulation tests
- [ ] CI
- [ ] CD
- [ ] container images
- [ ] Kubernetes manifests
- [ ] environment configuration
- [ ] secrets configuration
- [ ] release versioning

## Required platform-wide state model
Every operational object that can affect safety or authorization must have explicit lifecycle states, transition guards, audit events, timestamps, actor/device identity, country scope and organization scope.

## Required common fields
For domain entities where applicable:
- id
- external_id
- country_id
- organization_id
- created_at
- updated_at
- created_by
- updated_by
- version
- status
- audit correlation id

## Required completion gates
A capability is not considered complete until:
1. Database model exists.
2. Alembic migration exists.
3. Domain/service implementation exists.
4. API contract exists.
5. Authorization policy exists.
6. Audit events exist.
7. Unit tests exist.
8. Integration tests exist where applicable.
9. OpenAPI documentation exists.
10. Docker/runtime configuration exists.
11. Observability exists.
12. Security controls exist.
13. Localization-ready messages exist.
14. Failure/degraded-mode behavior is defined.
15. README/module documentation exists.

## Implementation order
1. Identity + authorization + sovereignty
2. PKI / machine identity
3. Organization / manufacturer / vehicle registry
4. Mission + Mission Graph
5. 3D GIS + corridor + airspace
6. Traffic control + route deviation
7. EmergencyOS
8. Telemetry + Digital Twin
9. Weather + Navigation + Energy
10. Vertiport + Maintenance
11. Regulation + Safety + Incident + Flight Recorder
12. Simulation
13. Integration/Event/Notification
14. Government/Manufacturer/Operator portals
15. AI platform and copilots
16. Passenger/Cargo/Marketplace/Billing
17. Multimodal mobility
18. Data/Analytics
19. Cybersecurity/Observability/DR/Edge hardening
20. Full certification-oriented validation and production readiness

## Definition of done for APEX/AMOS v1
A v1 release is complete only when a verified organization can register a certified vehicle, authenticate a human operator and machine, create and authorize a mission, generate a 3D route/corridor, evaluate weather/energy/risk, obtain country-scoped traffic clearance, execute telemetry, detect deviation/conflict/emergency, select a safe landing/corridor, record an immutable mission history, and expose only authorized country-scoped data to each participant.

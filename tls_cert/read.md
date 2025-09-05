To generate a key file:
openssl genrsa -out learner.key 2048

To generate a csr file:
openssl req -new -key learner.key -out learner.csr -subj "/CN=learner"


To update csr key to csr.yaml:
We need to convert learner.csr into base64 format and then use in csr.yaml
cat learner.csr | base64 | tr -d "\n"


csr.yaml:
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: learner-csr
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBS... (base64 encoded CSR)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400   # 1 day (optional)
  usages:
  - client auth

Then apply the certicates:
kubectl apply -f learner.csr 

To list the certificates:
kubectl get certificates


To approve a csr:
kubectl certificate approve <cert-name>

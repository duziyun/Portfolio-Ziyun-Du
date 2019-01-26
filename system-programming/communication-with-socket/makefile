all: rpc manage compute report
rpc: structs.x
	rpcgen structs.x
manage: manage.c
	cc manage.c structs_xdr.c -Wall -o manage
compute: compute.c
	cc compute.c structs_xdr.c -Wall -pthread -o compute
report: report.c
	cc report.c structs_xdr.c -Wall -o report
clean:
	rm compute manage structs.h structs_xdr.c report

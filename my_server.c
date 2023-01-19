#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

void * connection_handler(void *);

int main(){
	int socket_desc, new_socket, c, *new_sock;
	struct sockaddr_in server, client;
	char *message;
	
	socket_desc = socket(AF_INET, SOCK_STREAM, 0);
	if(socket_desc == -1){
		printf("could not create socket");
		exit(EXIT_FAILURE);
	}
	
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons(8000);
	
	if(bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0){
		puts("bind failed");
		exit(EXIT_FAILURE);
	}
	puts("bind done");
	
	listen(socket_desc, 3);
	
	puts("waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while((new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c))){
		puts("connection accepted");
		
		message = "Hello Client\n";
		write(new_socket, message, strlen(message));
		
		pthread_t sniffer_thread;
		new_sock = (int *)malloc(sizeof(int));
		*new_sock = new_socket;
		
		if(pthread_create(&sniffer_thread, NULL, connection_handler, (void *)new_sock) < 0){
			perror("could not create thread");
			return 1;
		}
		
		pthread_join(sniffer_thread, NULL);
		puts("handler assigned");
	}
	
	if(new_socket < 0){
	perror("accept failed");
	return 1;
	}
	
	return 0;
}

void *connection_handler(void * socket_desc){
	int sock = *(int *)socket_desc;
	int read_size;
	char message[2000], client_message[2000], schat[2000], *bye, s[10], chat[2000], s1[100];
	bye = "bye";
	
	strcpy(message, "To ");
	sprintf(s, "%d", sock);
	strncat(message, s, strlen(s));
	strcpy(s1, " : Greetings! I am your connection handler\n");
	strncat(message, s1, strlen(s1));
	write(sock, message, strlen(message));
	memset(message, 0, sizeof(message));
	read_size = read(sock, client_message, strlen(client_message));
	printf("From Client [%d] : %s\n", sock, client_message);
	strcpy(message, "To ");
	sprintf(s, "%d", sock);
	strncat(message, s, strlen(s));
	strcpy(s1, "Now we shall have a chat session: so type something \n");
	strncat(message, s1, strlen(s1));
	write(sock, message, strlen(message));
	
	while(1){
		memset(client_message, 0, sizeof(client_message));
		read_size = read(sock, client_message, strlen(client_message));
		printf("From Client [%d] : %s\n", sock, client_message);
		memset(schat, 0, sizeof(schat));
		printf("serveer : ");
		fgets(schat, sizeof(schat), stdin);
		strcpy(chat, "To ");
		sprintf(s, "%d", sock);
		strncat(chat, s, strlen(s));
		strncat(chat, schat, strlen(schat));
		send(sock, chat, strlen(chat), 0);
		schat[strlen(schat)] = '\0';
		if(strncmp(schat, bye, strlen(bye)) == 0){
			break;
		}
	}
	
	puts("Client disconnected");
	fflush(stdout);
	free(socket_desc);
	return 0;
}

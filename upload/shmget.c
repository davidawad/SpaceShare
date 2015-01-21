#include	<sys/types.h>
#include	<sys/ipc.h>
#include	<sys/shm.h>
#include	<errno.h>
#include	<stdio.h>
#include	<stdlib.h>
#include	<string.h>

// Playing with who gets a shared memory segment first.  Exercising shmat(), shmdt().
// Does time-consuming initialization of shared memory space.

int main(){
	key_t		key;
	int		shmid;
	char *p;
	int	size = 4096;
	char message[] = "Look at the guy next to you and wake him up.\n";

	if ( errno = 0, (key = ftok( "/put/your/own/path/here", 42 )) == -1 ){
		printf( "ftok() failed  errno :  %s\n", strerror( errno ) );
		exit( 1 );
	}
	else if (errno = 0, (shmid = shmget( key, size, 0666 | IPC_CREAT | IPC_EXCL )) != -1 ){		// create ok?
		errno = 0;
		p = (char *)shmat( shmid, 0, 0 );
		if ( p == (void *)-1 ){
			printf( "shmat() failed  errno :  %s\n", strerror( errno ) );
			exit( 1 );
		}
		else{
			// Successful creation of shared memory segment.  Segment is filled with zeros.
			// Do some interesting initialization.  Something that takes a while.
			sleep( 10 );
			printf( "Process %d puts message in created shared memory segment attached at address %#x.\n",
				getpid(), p + sizeof(int) );
			sprintf( p + sizeof(int), "%s", message );
			*p = 1;
			shmdt( p );
		}
	}
	else if (errno = 0, (shmid = shmget( key, 0, 0666 )) != -1 ){// find ok?
		errno = 0;
		p = (char *)shmat( shmid, 0, 0 );
		if ( p == (void *)-1 ){
			printf( "shmat() failed  errno :  %s\n", strerror( errno ) );
			exit( 1 );
		}
		else{
			// Acquired shared memory segment.  Has to wait until segment is properly initialized by creator.
			// Could spin around until initialization complete.
			while ( *p == 0 ){
				printf( "\x1b[2;32mFound segment waiting for initialization to complete.\x1b[0m\n" );
			}
			printf( "Process %d gets message from shared memory segment attached at address %#x.\n", getpid(), p );
			printf( "\n%s\n", p + sizeof(int) );
			shmdt( p );
		}
	}
	else{// no create, no find
		printf( "shmget() failed  errno :  %s\n", strerror( errno ) );
		exit( 1 );
	}
	printf( "normal end.\n" );
	return 0;
}

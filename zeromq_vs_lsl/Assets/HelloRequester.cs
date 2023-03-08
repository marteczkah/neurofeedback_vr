// class responsible for the communication with Python

using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

/// <summary>
///     Example of requester who only sends Hello. Very nice guy.
///     You can copy this class and modify Run() to suits your needs.
///     To use this class, you just instantiate, call Start() when you want to start and Stop() when you want to stop.
/// </summary>
public class HelloRequester : RunAbleThread
{
    /// <summary>
    ///     Request Hello message to server and receive message back. Do it 10 times.
    ///     Stop requesting when Running=false.
    /// </summary>
    public string current_msg = "rest";

    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
	    // change this depending on the IP of the Oculus device, the port can stay as 5555
            client.Connect("tcp://localhost:5555");

	    while (Running) {
              Debug.Log("Sending Request");
              client.SendFrame("Request");
              string message = null;
              bool gotMessage = false;	
	      current_msg = "rest"; // initializing the message as "rest" state
	      
	      // loop that checks if there is a message coming, breaks when there is a message
	      while (Running) 
	      {
		    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                    if (gotMessage) break;
	      }
	      if (gotMessage) {
		    Debug.Log("Received " + message);
		    current_msg = message; // saving the message so it can be read by outside files
	      }
	    }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}

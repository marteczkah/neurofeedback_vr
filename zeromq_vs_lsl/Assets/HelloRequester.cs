// class responsible for the communication with Python
using System.Collections;
using System.Collections.Generic;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;
using System;
using System.IO;

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
    public string current_msg = "";
    public string milliseconds;
    public List<string> msgs = new List<string>();
    public List<string> times = new List<string>();
    private StreamWriter writer;
    public string filePath = "ms.csv";
    public int num_msgs = 50;
    private int count_msgs = 0;

    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
	    // change this depending on the IP of the Oculus device, the port can stay as 5555
            client.Connect("tcp://localhost:5555");

	    while (count_msgs < num_msgs) {
              Debug.Log("Sending Request");
              client.SendFrame("Request");
              string message = null;
              bool gotMessage = false;	
	          current_msg = "rest"; // initializing the message as "rest" state
	      
	      // loop that checks if there is a message coming, breaks when there is a message
	      while (Running) 
	      {
		    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                    if (gotMessage) 
                    {
                        milliseconds = DateTime.Now.ToString("hh.mm.ss.ffffff");
                        break;
                    }
	      }
	      if (gotMessage) {
            times.Add(milliseconds);
            msgs.Add(message);
		    Debug.Log("Received " + message);
		    current_msg = message; // saving the message so it can be read by outside files
            num_msgs += 1;
            if (message.Equals("end"))
            {
                break;
            }
          }
	    }
        }
        writer = new StreamWriter(filePath);
        writer.WriteLine("Time,Msg");
        for (int i = 0; i < Mathf.Max(times.Count, msgs.Count); ++i)
            {
                if (i < times.Count) writer.Write(times[i]);
                writer.Write(",");
                if (i < msgs.Count) writer.Write(msgs[i]);
                writer.Write(System.Environment.NewLine);
            }
        writer.Flush();
        writer.Close();

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}

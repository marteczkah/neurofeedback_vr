// script for making the right bullet shoot based on the message sent from Python

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReadZeroMQ : MonoBehaviour
{
    private HelloRequester _helloRequester;

    // Start is called before the first frame update
    void Start()
    {
	// initializing HelloRequester class
	    _helloRequester = new HelloRequester();
        _helloRequester.Start();
    }

    // Update is called once per frame
    void Update()
    {
	// bullet fired only when the message coming says right	
        Debug.Log(_helloRequester.current_msg);
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}
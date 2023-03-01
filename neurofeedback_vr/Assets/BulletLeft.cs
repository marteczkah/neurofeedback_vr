// script for making the left bullet shoot based on the message sent from Python

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class BulletLeft : MonoBehaviour
{
    public GameObject bullet;
    public Transform spawnPoint; // the transformation to make the bullet go from the end of the gun
    public float fireSpeed = 20;
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
	// bullet fired only when the message coming says left	
       if (_helloRequester.current_msg == "left") {
	FireBullet();
	print(_helloRequester.current_msg);
       } 
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }

    // function for firing the bullet
    public void FireBullet()
    {
	GameObject spawnedBullet = Instantiate(bullet);
	spawnedBullet.transform.position = spawnPoint.position;
	spawnedBullet.GetComponent<Rigidbody>().velocity = spawnPoint.forward * fireSpeed;
	Destroy(spawnedBullet, 5);
    }
}

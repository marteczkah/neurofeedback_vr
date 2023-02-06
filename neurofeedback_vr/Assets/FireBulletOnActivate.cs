using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class FireBulletOnActivate : MonoBehaviour
{
    public GameObject bullet;
    public Transform spawnPoint;
    public float fireSpeed = 20;
    private HelloRequester _helloRequester;

    // Start is called before the first frame update
    void Start()
    {
	XRGrabInteractable grabbable = GetComponent<XRGrabInteractable>();
	grabbable.activated.AddListener(FireBullet);
	_helloRequester = new HelloRequester();
        _helloRequester.Start();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }

    public void FireBullet(ActivateEventArgs arg)
    {
	GameObject spawnedBullet = Instantiate(bullet);
	spawnedBullet.transform.position = spawnPoint.position;
	spawnedBullet.GetComponent<Rigidbody>().velocity = spawnPoint.forward * fireSpeed;
	Destroy(spawnedBullet, 5);
    }
}

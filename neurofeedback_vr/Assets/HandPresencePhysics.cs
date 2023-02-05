using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandPresencePhysics : MonoBehaviour
{
    public Transform target;
    private Rigidbody rb;
    private Collider[] handColliders;
    public Renderer nonPhysicalHand; 


    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        handColliders = GetComponentsInChildren<Collider>();
        nonPhysicalHand.enabled = false;
    }

    public void EnableHandCollider()
    {
    	foreach (var item in handColliders)
        {
	   item.enabled = true;
        }

    }

    public void EnableHandColliderDelay(float delay)
    {
	Invoke("EnableHandCollider", delay);
    }

    public void DisableHandCollider()
    {
        foreach (var item in handColliders)
        {
	   item.enabled = false;
        }

    }

    // Update is called once per frame
    void FixedUpdate()
    {
	// position
        rb.velocity = (target.position - transform.position) / Time.fixedDeltaTime;

	//ROTATION
	Quaternion rotationDifference = target.rotation * Quaternion.Inverse(transform.rotation);
	rotationDifference.ToAngleAxis(out float angleInDegree, out Vector3 rotationAxis);

	Vector3 rotationDifferenceInDegree = angleInDegree * rotationAxis;

	rb.angularVelocity = (rotationDifferenceInDegree * Mathf.Deg2Rad / Time.fixedDeltaTime);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class moveBox : MonoBehaviour
{
    public bool moved_left;
    // Start is called before the first frame update
    void Start()
    {
     	moved_left = true;   
    }

    // Update is called once per frame
    void Update()
    {
	Vector3 position = this.transform.position;
	if (moved_left) {
		position.x--;
		moved_left = false;
	} else {
		position.x++;
		moved_left = true;
	}
        this.transform.position = position;
    }
}

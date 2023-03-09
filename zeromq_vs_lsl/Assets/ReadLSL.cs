using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using LSL;
using System;
using System.IO;

namespace LSL4Unity.Samples.SimpleInlet
{ 
    // You probably don't need this namespace. We do it to avoid contaminating the global namespace of your project.
    public class ReadLSL : MonoBehaviour
    {
        /*
         * This example shows the minimal code required to get an LSL inlet running
         * without leveraging any of the helper scripts that come with the LSL package.
         * This behaviour uses LSL.cs only. There is little-to-no error checking.
         * See Resolver.cs and BaseInlet.cs for helper behaviours to make your implementation
         * simpler and more robust.
         */

        // We need to find the stream somehow. You must provide a StreamName in editor or before this object is Started.
        public string StreamName;
        ContinuousResolver resolver;

        double max_chunk_duration = 0.2;  // Duration, in seconds, of buffer passed to pull_chunk. This must be > than average frame interval.

        // We need to keep track of the inlet once it is resolved.
        private StreamInlet inlet;

        // We need buffers to pass to LSL when pulling data.
        private float[,] data_buffer;  // Note it's a 2D Array, not array of arrays. Each element has to be indexed specifically, no frames/columns.
        private double[] timestamp_buffer;
        private StreamWriter writer;
        public string filePath;
        public List<string> msgs = new List<string>();
        public List<string> times = new List<string>();

        void Start()
        {
            filePath = "save.csv";
            if (!StreamName.Equals(""))
                resolver = new ContinuousResolver("name", StreamName);
            else
            {
                Debug.LogError("Object must specify a name for resolver to lookup a stream.");
                this.enabled = false;
                return;
            }
            StartCoroutine(ResolveExpectedStream());
            writer = new StreamWriter(filePath);
        }

        IEnumerator ResolveExpectedStream()
        {

            var results = resolver.results();
            while (results.Length == 0)
            {
                yield return new WaitForSeconds(.1f);
                results = resolver.results();
            }

            inlet = new StreamInlet(results[0]);
            results.DisposeArray();

            // Prepare pull_chunk buffer
            int buf_samples = (int)Mathf.Ceil((float)(inlet.info().nominal_srate() * max_chunk_duration));
            Debug.Log("Allocating buffers to receive " + buf_samples + " samples.");
            int n_channels = inlet.info().channel_count();
            data_buffer = new float[buf_samples, n_channels];
            timestamp_buffer = new double[buf_samples];
        }

        // Update is called once per frame
        void Update()
        {
            string[] sample = new string[1];
            if (inlet != null)
            {
                inlet.pull_sample(sample);
                string milliseconds = DateTime.Now.ToString("hh.mm.ss.ffffff");
                times.Add(milliseconds);
                msgs.Add(sample[0]);
                Debug.Log("received sample " + sample[0]);
                if (sample[0].Equals("end"))
                {
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
                }
            }
        }
    }
}
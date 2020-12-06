using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Xml;
using UnityEngine;

public class TrackExporter
{

    public TrackExporter()
    {
    }

    public void SimpleExport(List<TrackParts> trackParts, string path)
    {
        float trackLength = 0;
        foreach (TrackParts tp in trackParts)
            trackLength += tp.Length;

        List<Geometry> gs = this.BuildGeometries(trackParts);

        XmlWriterSettings settings = new XmlWriterSettings();
        settings.Indent = true;
        settings.NewLineChars = "\n";
        settings.Encoding = new UTF8Encoding(false);

        XmlWriter xw = XmlWriter.Create(path, settings);
        xw.WriteStartDocument(true);

        xw.WriteStartElement("OpenDRIVE");
        // HEADER
        xw.WriteStartElement("header");
        xw.WriteAttributeString("revMajor", "1");
        xw.WriteAttributeString("revMinor", "4");
        xw.WriteAttributeString("name", "");
        xw.WriteAttributeString("version", "1");
        xw.WriteAttributeString("date", "");
        xw.WriteAttributeString("north", "0.0");
        xw.WriteAttributeString("south", "0.0");
        xw.WriteAttributeString("east", "0.0");
        xw.WriteAttributeString("west", "0.0");
        xw.WriteFullEndElement();

        xw.WriteStartElement("road");
        xw.WriteAttributeString("name", "TestTrack");
        xw.WriteAttributeString("length", trackLength.ToString().Replace(',', '.'));
        xw.WriteAttributeString("id", "1");
        xw.WriteAttributeString("junction", "-1");
        xw.WriteStartElement("link");
        xw.WriteFullEndElement(); // End link

        // Road -> Type
        xw.WriteStartElement("type");
        xw.WriteAttributeString("s", "0.0"); // starting point
        xw.WriteAttributeString("type", "town");
        xw.WriteFullEndElement(); // End Type

        xw.WriteStartElement("planView");

        foreach(Geometry g in gs)
        {
            // Road -> PlanView -> Geometry
            xw.WriteStartElement("geometry");
            xw.WriteAttributeString("s", g.geometry_s.ToString().Replace(',', '.'));
            xw.WriteAttributeString("x", g.geometry_x.ToString().Replace(',', '.'));
            xw.WriteAttributeString("y", g.geometry_y.ToString().Replace(',', '.'));
            xw.WriteAttributeString("hdg", g.geometry_hdg.ToString().Replace(',', '.'));
            xw.WriteAttributeString("length", g.geometry_length.ToString().Replace(',', '.'));

            if (g.geo_type == "line") // line
            {

                xw.WriteStartElement("line");
                xw.WriteEndElement();
            }
            else if (g.geo_type == "arc") // arc
            {
                xw.WriteStartElement("arc");
                xw.WriteAttributeString("curvature", g.geometry_arc_curv.ToString().Replace(',', '.'));
                xw.WriteEndElement();
            }

            xw.WriteFullEndElement(); // End Geometry
        }

        xw.WriteFullEndElement(); // End planView

        xw.WriteEndDocument();
        xw.Close();
    }

    private List<Geometry> BuildGeometries(List<TrackParts> tps)
    {
        List<Geometry> geometries = new List<Geometry>();

        float s = 0;
        for (int i = 0; i < tps.Count; i++)
        {
            TrackParts tp = tps[i];

            Geometry g = new Geometry();
            g.geometry_s = s;
            g.geometry_length = Mathf.Abs(tp.Length);
            g.geometry_x = tp.Start.x;
            g.geometry_y = tp.Start.y;
            
            if (tp is Straight)
            {
                g.geometry_hdg = Mathf.Atan2(tp.End.y - tp.Start.y, tp.End.x - tp.Start.x);
                g.geo_type = "line";
            }
            else
            {
                g.geo_type = "arc";
                TrackParts tpBefore = tps[(i - 1) % tps.Count];
                g.geometry_hdg = Mathf.Atan2(tp.Start.y - tpBefore.Start.y, tp.Start.x - tpBefore.Start.x);
                g.geometry_arc_curv = (tp as Arc).Curvature;
            }

            s += tps[i].Length;
            geometries.Add(g);
        }

        return geometries;
    }
}

public class Geometry
{
    public string geo_type = "line"; // "spiral", "arc" 
    public double geometry_s = 0;
    public double geometry_x = 0.045708987861871719;
    public double geometry_y = -125.5;
    public double geometry_hdg = 1.5711605548858643;
    public double geometry_length = 251.00001525878906;
    public double geometry_arc_curv = 4.8660000002386400e-01;
}
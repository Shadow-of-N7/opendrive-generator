using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class TrackParts
{
    public Vector2 Start;
    public Vector2 End;
    public float Length;
}

public class Straight : TrackParts
{
    public Straight(Vector2 start, Vector2 end)
    {
        Start = start;
        End = end;
        Length = (end - start).magnitude;
    }
}

public class Arc : TrackParts
{
    public Arc(Vector2 start, Vector2 end, float curvature, float length)
    {
        Start = start;
        End = end;
        Curvature = curvature;
        Length = length;
    }

    public Arc(Vector2 start, Vector2 end, float curvature, float length, Vector2 middlePoint)
    {
        Start = start;
        End = end;
        Curvature = curvature;
        Length = length;
        MiddlePoint = middlePoint;
    }

    public float Curvature { get; private set; }
    public Vector2 MiddlePoint { get; private set; }
}
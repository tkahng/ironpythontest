#   private void RunScript(bool iReset, List<Point3d> iStartingPositions, int iMaxCenterCount, ref object oCenters)
#   {
#     if (iReset || centers == null)
#       centers = new List<Point3d>(iStartingPositions);

#     List<Vector3d> totalMoves = new List<Vector3d>();
#     List<double> collisionCounts = new List<double>();

#     for (int i = 0; i < centers.Count; i++)
#     {
#       totalMoves.Add(new Vector3d(0.0, 0.0, 0.0));
#       collisionCounts.Add(0.0);
#     }

#     double collisionDistance = 2.0;

#     for (int i = 0; i < centers.Count; i++)
#       for (int j = i + 1; j < centers.Count; j++)
#       {
#         double d = centers[i].DistanceTo(centers[j]);
#         if (d > collisionDistance) continue;
#         Vector3d move = centers[i] - centers[j];
#         if (move.Length < 0.001) continue;
#         move.Unitize();
#         move *= 0.5 * (collisionDistance - d);
#         totalMoves[i] += move;
#         totalMoves[j] -= move;
#         collisionCounts[i] += 1.0;
#         collisionCounts[j] += 1.0;
#       }

#     for (int i = 0; i < centers.Count; i++)
#       if (collisionCounts[i] != 0.0)
#         centers[i] += totalMoves[i] / collisionCounts[i];

#     if (centers.Count < iMaxCenterCount)
#     {
#       List<int> splitIndices = new List<int>();

#       for (int i = 0; i < centers.Count - 1; i++)
#         if (centers[i].DistanceTo(centers[i + 1]) > 1.99)
#           splitIndices.Add(i + 1 + splitIndices.Count);

#       foreach (int splitIndex in splitIndices)
#       {
#         Point3d newCenter = 0.5 * (centers[splitIndex - 1] + centers[splitIndex]);
#         centers.Insert(splitIndex, newCenter);
#       }
#     }


#     oCenters = centers;
#   }

#   // <Custom additional code> 


#   List<Point3d> centers;

import rhinoscriptsyntax as rs

if iReset:
    centers = iStartingPositions
    
totalMoves = []
collisionCounts = []

for i in range(len(centers)):
    
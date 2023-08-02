from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Body, Depends, status, HTTPException, Path, Query
from sqlmodel import Session, select

from ..auth import get_current_user
from ..database import get_session
from ..schemas import RecommendationCreate, RecommendationRead, RecommendationUpdate
from ..models import Tag, User, Recommendation, FictionType
